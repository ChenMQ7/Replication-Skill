"""Check embedded starters; regenerate copies only with --write."""
import argparse
import sys
from skill_files import SKILL_ROOT, embedded_templates, template_errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regenerate template copies in this skill folder. Never edits runs.')
    args = parser.parse_args(argv)
    try:
        if args.write:
            embedded = embedded_templates()
            folder = SKILL_ROOT / 'templates'
            # Validate all destinations before writing any file.
            if folder.is_symlink() or not folder.is_dir():
                raise ValueError('The template directory must be a real directory.')
            for name in embedded:
                path = folder / name
                if path.is_symlink() or (path.exists() and not path.is_file()):
                    raise ValueError(f'Unsafe template destination: {name}')
            for name, body in embedded.items():
                (folder / name).write_text(body, encoding='utf-8')
        errors = template_errors()
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
        print(f'{len(embedded_templates())} template copies match SKILL.md.')
        return 0
    except (OSError, ValueError, IndexError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
