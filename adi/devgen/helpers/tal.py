# Helpers for dealing with TAL, Zope's Template-Attribute-Language.

from zope.tal.dummyengine import DummyEngine
from zope.tal.htmltalparser import HTMLTALParser
from zope.tal.talgenerator import TALGenerator
from zope.tal.talinterpreter import TALInterpreter
from StringIO import StringIO

def talToHtml(tal):
    """
    Expects TAL-string, returns interpreted HTML-string.
    Works only with string-(and python?)-expressions, not
    with path-expressions.
    """
    generator = TALGenerator(xml=0, source_file=None)
    parser = HTMLTALParser(generator)
    parser.parseString(tal)
    program, macros = parser.getCode()
    engine = DummyEngine(macros)
    result = StringIO()
    interpreter = TALInterpreter(program, {}, engine, stream=result)
    interpreter()
    tal = result.getvalue().strip()
    return tal

