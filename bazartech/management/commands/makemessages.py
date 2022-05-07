import os
import shutil
from importlib import import_module
from pathlib import Path

from django.apps.registry import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.makemessages import (
    NO_LOCALE_DIR,
    STATUS_OK,
    Command as MakeMessagesCommand,
    NamedTemporaryFile,
    normalize_eols,
    write_pot_file,
)
from django.core.management.utils import DEFAULT_LOCALE_ENCODING, PIPE, run


# Modified version of django.core.management.utils.popen_wrapper to include cwd argument
def popen_wrapper(args, stdout_encoding="utf-8", **kwargs):
    """
    Friendly wrapper around Popen.

    Return stdout output, stderr output, and OS status code.
    """
    try:
        p = run(args, stdout=PIPE, stderr=PIPE, close_fds=os.name != "nt", **kwargs)
    except OSError as err:
        raise CommandError("Error executing %s" % args[0]) from err
    return (p.stdout.decode(stdout_encoding), p.stderr.decode(DEFAULT_LOCALE_ENCODING, errors="replace"), p.returncode)


# Wrapper to django default command 'makemessages'
# In this project, a app_label must be provided in order to generate message files to this given app.
class Command(MakeMessagesCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("app", help="Name of the application or project.")

    def check_app(self, app_label):
        try:
            apps.get_app_config(app_label)
        except LookupError as ex:
            raise CommandError(ex)

    @property
    def _local_app(self):
        return self._app_label in settings.LOCAL_APPS

    @property
    def default_locale_path(self):
        if self._local_app:
            return os.path.join(self._app_path, "locale")
        else:
            return os.path.join(settings.PROJECT_ROOT, "translation", self._app_label, "locale")

    @default_locale_path.setter
    def default_locale_path(self, value):
        pass

    def handle(self, *args, **options):
        self.check_app(options.get("app"))
        self._app_label = options.pop("app")
        self._app_path = import_module(self._app_label).__path__[0]
        self._execution_path = str(Path(self._app_path).parent)

        if self.default_locale_path not in settings.LOCALE_PATHS and not self._local_app:
            raise CommandError(
                f'Please add "{os.path.relpath(self.default_locale_path, settings.BASE_DIR)}"'
                f" in the LOCALE_PATHS setting."
            )

        super().handle(*args, **options)

    def write_po_file(self, potfile, locale):
        """
        Create or update the PO file for self.domain and `locale`.
        Use contents of the existing `potfile`.

        Use msgmerge and msgattrib GNU gettext utilities.
        """
        basedir = os.path.join(os.path.dirname(potfile), locale, "LC_MESSAGES")
        os.makedirs(basedir, exist_ok=True)
        app_pofile = pofile = os.path.join(basedir, "%s.po" % self.domain)
        app_local_pofile = os.path.join(self._app_path, "locale", locale, "LC_MESSAGES", "%s.po" % self.domain)

        if not os.path.exists(pofile) and not self._local_app and os.path.exists(app_local_pofile):
            pofile = app_local_pofile

        if os.path.exists(pofile):
            args = ["msgmerge"] + self.msgmerge_options + [pofile, potfile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise CommandError("errors happened while running msgmerge\n%s" % errors)
                elif self.verbosity > 0:
                    self.stdout.write(errors)

            if pofile != app_pofile:
                shutil.copy(pofile, app_pofile)
        else:
            with open(potfile, encoding="utf-8") as fp:
                msgs = fp.read()
            if not self.invoked_for_django:
                msgs = self.copy_plural_forms(msgs, locale)
        msgs = normalize_eols(msgs)
        msgs = msgs.replace("#. #-#-#-#-#  %s.pot (PACKAGE VERSION)  #-#-#-#-#\n" % self.domain, "")
        with open(pofile, "w", encoding="utf-8") as fp:
            fp.write(msgs)

        if self.no_obsolete:
            args = ["msgattrib"] + self.msgattrib_options + ["-o", pofile, pofile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise CommandError("errors happened while running msgattrib\n%s" % errors)
                elif self.verbosity > 0:
                    self.stdout.write(errors)

    def process_locale_dir(self, locale_dir, files):
        """
        Extract translatable literals from the specified files, creating or
        updating the POT file for a given locale directory.

        Use the xgettext GNU gettext utility.
        """
        build_files = []
        for translatable in files:
            if self.verbosity > 1:
                self.stdout.write("processing file %s in %s\n" % (translatable.file, translatable.dirpath))
            if self.domain not in ("djangojs", "django"):
                continue
            build_file = self.build_file_class(self, self.domain, translatable)
            try:
                build_file.preprocess()
            except UnicodeDecodeError as e:
                self.stdout.write(
                    "UnicodeDecodeError: skipped file %s in %s (reason: %s)"
                    % (translatable.file, translatable.dirpath, e)
                )
                continue
            build_files.append(build_file)

        if self.domain == "djangojs":
            is_templatized = build_file.is_templatized
            args = [
                "xgettext",
                "-d",
                self.domain,
                "--language=%s" % ("C" if is_templatized else "JavaScript",),
                "--keyword=gettext_noop",
                "--keyword=gettext_lazy",
                "--keyword=ngettext_lazy:1,2",
                "--keyword=pgettext:1c,2",
                "--keyword=npgettext:1c,2,3",
                "--output=-",
            ]
        elif self.domain == "django":
            args = [
                "xgettext",
                "-d",
                self.domain,
                "--language=Python",
                "--keyword=gettext_noop",
                "--keyword=gettext_lazy",
                "--keyword=ngettext_lazy:1,2",
                "--keyword=ugettext_noop",
                "--keyword=ugettext_lazy",
                "--keyword=ungettext_lazy:1,2",
                "--keyword=pgettext:1c,2",
                "--keyword=npgettext:1c,2,3",
                "--keyword=pgettext_lazy:1c,2",
                "--keyword=npgettext_lazy:1c,2,3",
                "--output=-",
            ]
        else:
            return

        input_files = [os.path.relpath(bf.work_path, self._execution_path) for bf in build_files]

        with NamedTemporaryFile(mode="w+") as input_files_list:
            input_files_list.write(("\n".join(input_files)))
            input_files_list.flush()
            args.extend(["--files-from", input_files_list.name])
            args.extend(self.xgettext_options)
            msgs, errors, status = popen_wrapper(args, cwd=self._execution_path)

        if errors:
            if status != STATUS_OK:
                for build_file in build_files:
                    build_file.cleanup()
                raise CommandError(
                    "errors happened while running xgettext on %s\n%s" % ("\n".join(input_files), errors)
                )
            elif self.verbosity > 0:
                # Print warnings
                self.stdout.write(errors)

        if msgs:
            if locale_dir is NO_LOCALE_DIR:
                file_path = os.path.normpath(build_files[0].path)
                raise CommandError("Unable to find a locale path to store translations for " "file %s" % file_path)
            for build_file in build_files:
                msgs = build_file.postprocess_messages(msgs)
            potfile = os.path.join(locale_dir, "%s.pot" % self.domain)
            write_pot_file(potfile, msgs)

        for build_file in build_files:
            build_file.cleanup()

    def find_app_files(self):
        file_list = self.find_files(self._app_path)

        template_folder = os.path.join(settings.PROJECT_ROOT, "templates", self._app_label)

        if os.path.exists(template_folder):
            file_list += self.find_files(template_folder)

        for file in file_list:
            file.locale_dir = self.default_locale_path

        return file_list

    def build_potfiles(self):
        """
        Build pot files and apply msguniq to them.
        """
        file_list = self.find_app_files()
        self.remove_potfiles()
        self.process_files(file_list)
        potfiles = []
        for path in self.locale_paths:
            potfile = os.path.join(path, "%s.pot" % self.domain)
            if not os.path.exists(potfile):
                continue
            args = ["msguniq"] + self.msguniq_options + [potfile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise CommandError("errors happened while running msguniq\n%s" % errors)
                elif self.verbosity > 0:
                    self.stdout.write(errors)
            msgs = normalize_eols(msgs)
            with open(potfile, "w", encoding="utf-8") as fp:
                fp.write(msgs)
            potfiles.append(potfile)

        return potfiles
