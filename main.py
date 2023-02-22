from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template_script.py')



def rewrite_to_camel_case_singular(word):
    words = word.split("_")
    words = [x.capitalize() for x in words]
    words[-1] = words[-1][:-1]
    return "".join(words)


def rewrite_to_lowercase_plural_docstrings(word):
    words = word.split("_")
    return " ".join(words)

def rewrite_to_lowercase_singular_docstrings(word):
    words = word.split("_")
    words[-1] = words[-1][:-1]
    return " ".join(words)


def rewrite_to_docstrings_name_camelcase_plural(word):
    words = word.split("_")
    words = [x.capitalize() for x in words]
    return " ".join(words)


names = ["color_palettes",]

for elem in names:
    name = elem
    camel_case_singular = rewrite_to_camel_case_singular(elem)
    name_singular = elem[:-1]
    docstrings_name_lower_case_plural =\
        rewrite_to_lowercase_plural_docstrings(elem)
    docstring_name_lower_case_singular =\
        rewrite_to_lowercase_singular_docstrings(elem)
    docstrings_name_camelcase_plural = \
        rewrite_to_docstrings_name_camelcase_plural(elem)

    output_from_parsed_template = template.render(name=name,
                                                  camel_case_singular=camel_case_singular,
                                                  name_singular=name_singular,
                                                  docstrings_name_lower_case_plural=docstrings_name_lower_case_plural,
                                                  docstring_name_lower_case_singular=docstring_name_lower_case_singular,
                                                  docstrings_name_camelcase_plural=docstrings_name_camelcase_plural)

    with open(f"templates/{name}.py", "w") as fh:
        fh.write(output_from_parsed_template)