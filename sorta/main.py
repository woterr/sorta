import typer


app = typer.Typer(help="sorta: Document sorter using keyword-based routing")

import sorta.commands.init
import sorta.commands.config
import sorta.commands.edit
import sorta.commands.list
import sorta.commands.classify
import sorta.commands.run
import sorta.commands.watch
import sorta.commands.sort
import sorta.commands.add_root
import sorta.commands.add_rule
import sorta.commands.doctor

## debug
# config = load_config()
# text = extract_pdf_text("/mnt/shared/Projects/sorta/test.pdf")

# print(classify(text, config))


def main():
    app()


if __name__ == "__main__":
    main()
