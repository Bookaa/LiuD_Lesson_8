# auto generated

# LiuD syntax :

# option.prefix = GDL01
#     states.skip = crlf
#     main = stmt*
#     stmt := declare_with_value | declare | assign | funccall
#     datatype = 'int' | 'long'
#     declare = datatype NAME
#     declare_with_value = datatype NAME '=' value
#     value0 = NUMBER | NAME
#     value1 := value0 | enclosed
#         enclosed = '(' value ')'
#     value2 := signed | value1
#         signed = ('-' | '+') value1
#     binvalue = value2 (, '**' ('*' '/') ('+' '-') ('>=' '>' '<=' '<' '==' '!=')) value1
#     value := binvalue
#     assign = NAME '=' value
#     funccall = NAME '(' value ')'
#     

from GDL_common import *

class GDL01_main:
    def __init__(self, vlst):
        self.vlst = vlst
    def walkabout(self, visitor):
        return visitor.visit_main(self)

class GDL01_datatype:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_datatype(self)

class GDL01_declare:
    def __init__(self, v, s):
        self.v = v
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_declare(self)

class GDL01_declare_with_value:
    def __init__(self, v1, s, v2):
        self.v1 = v1
        self.s = s
        self.v2 = v2
    def walkabout(self, visitor):
        return visitor.visit_declare_with_value(self)

class GDL01_value0:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_value0(self)

class GDL01_enclosed:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_enclosed(self)

class GDL01_signed:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_signed(self)

class GDL01_binvalue:
    def __init__(self, v1, s, v2):
        self.v1 = v1
        self.s = s
        self.v2 = v2
    def walkabout(self, visitor):
        return visitor.visit_binvalue(self)

class GDL01_assign:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_assign(self)

class GDL01_funccall:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_funccall(self)

class GDL01_Parser(Parser00):

    def handle_main(self):
        v = self.hdl_stmt()
        if not v:
            return None
        savpos = self.pos
        vlst = [v]
        while True:
            self.skipspacecrlf()
            v = self.hdl_stmt()
            if not v:
                break
            vlst.append(v)
            savpos = self.pos
        self.restorepos(savpos)
        return GDL01_main(vlst)

    def hdl_stmt(self):
        v = self.handle_declare_with_value()
        if not v:
            v = self.handle_declare()
        if not v:
            v = self.handle_assign()
        if not v:
            v = self.handle_funccall()
        if not v:
            return None
        return v

    def handle_datatype(self):
        s = self.handle_str('int')
        if not s:
            s = self.handle_str('long')
        if not s:
            return None
        return GDL01_datatype(s)

    def handle_declare(self):
        savpos = self.pos
        v = self.handle_datatype()
        if not v:
            return None
        self.skipspacecrlf()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        return GDL01_declare(v, s)

    def handle_declare_with_value(self):
        savpos = self.pos
        v1 = self.handle_datatype()
        if not v1:
            return None
        self.skipspacecrlf()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v2 = self.hdl_value()
        if not v2:
            return self.restorepos(savpos)
        return GDL01_declare_with_value(v1, s, v2)

    def handle_value0(self):
        s = self.handle_NUMBER()
        if not s:
            s = self.handle_NAME()
        if not s:
            return None
        return GDL01_value0(s)

    def hdl_value1(self):
        v = self.handle_value0()
        if not v:
            v = self.handle_enclosed()
        if not v:
            return None
        return v

    def handle_enclosed(self):
        savpos = self.pos
        if not self.handle_str('('):
            return None
        self.skipspacecrlf()
        v = self.hdl_value()
        if not v:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        if not self.handle_str(')'):
            return self.restorepos(savpos)
        return GDL01_enclosed(v)

    def hdl_value2(self):
        v = self.handle_signed()
        if not v:
            v = self.hdl_value1()
        if not v:
            return None
        return v

    def handle_signed(self):
        savpos = self.pos
        s = self.handle_str('-')
        if not s:
            s = self.handle_str('+')
        if not s:
            return None
        self.skipspacecrlf()
        v = self.hdl_value1()
        if not v:
            return self.restorepos(savpos)
        return GDL01_signed(s, v)

    def handle_binvalue(self):
        v1 = self.hdl_value2()
        if not v1:
            return None
        def multiop1(v1):
            while True:
                savpos = self.pos
                self.skipspacecrlf()
                for s in ['**']:
                    if self.handle_str(s):
                        break
                else:
                    self.restorepos(savpos)
                    return v1
                self.skipspacecrlf()
                v2 = self.hdl_value1()
                if not v2:
                    self.restorepos(savpos)
                    return v1
                v1 = GDL01_binvalue(v1, s, v2)
        def multiop2(v1):
            v1 = multiop1(v1)
            while True:
                savpos = self.pos
                self.skipspacecrlf()
                for s in ['*', '/']:
                    if self.handle_str(s):
                        break
                else:
                    self.restorepos(savpos)
                    return v1
                self.skipspacecrlf()
                v2 = self.hdl_value1()
                if not v2:
                    self.restorepos(savpos)
                    return v1
                v2 = multiop1(v2)
                v1 = GDL01_binvalue(v1, s, v2)
        def multiop3(v1):
            v1 = multiop2(v1)
            while True:
                savpos = self.pos
                self.skipspacecrlf()
                for s in ['+', '-']:
                    if self.handle_str(s):
                        break
                else:
                    self.restorepos(savpos)
                    return v1
                self.skipspacecrlf()
                v2 = self.hdl_value1()
                if not v2:
                    self.restorepos(savpos)
                    return v1
                v2 = multiop2(v2)
                v1 = GDL01_binvalue(v1, s, v2)
        def multiop4(v1):
            v1 = multiop3(v1)
            while True:
                savpos = self.pos
                self.skipspacecrlf()
                for s in ['>=', '>', '<=', '<', '==', '!=']:
                    if self.handle_str(s):
                        break
                else:
                    self.restorepos(savpos)
                    return v1
                self.skipspacecrlf()
                v2 = self.hdl_value1()
                if not v2:
                    self.restorepos(savpos)
                    return v1
                v2 = multiop3(v2)
                v1 = GDL01_binvalue(v1, s, v2)
        return multiop4(v1)

    def hdl_value(self):
        v = self.handle_binvalue()
        if not v:
            return None
        return v

    def handle_assign(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspacecrlf()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v = self.hdl_value()
        if not v:
            return self.restorepos(savpos)
        return GDL01_assign(s, v)

    def handle_funccall(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspacecrlf()
        if not self.handle_str('('):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v = self.hdl_value()
        if not v:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        if not self.handle_str(')'):
            return self.restorepos(savpos)
        return GDL01_funccall(s, v)

class GDL01_output:
    def __init__(self, outp):
        self.outp = outp
    def visit_main(self, node):
        for v in node.vlst:
            v.walkabout(self)
    def visit_stmt(self, node):
        node.v.walkabout(self)
    def visit_datatype(self, node):
        self.outp.puts(node.s)
    def visit_declare(self, node):
        node.v.walkabout(self)
        self.outp.puts(node.s)
    def visit_declare_with_value(self, node):
        node.v1.walkabout(self)
        self.outp.puts(node.s)
        self.outp.puts('=')
        node.v2.walkabout(self)
    def visit_value0(self, node):
        self.outp.puts(node.s)
    def visit_value1(self, node):
        node.v.walkabout(self)
    def visit_enclosed(self, node):
        self.outp.puts('(')
        node.v.walkabout(self)
        self.outp.puts(')')
    def visit_value2(self, node):
        node.v.walkabout(self)
    def visit_signed(self, node):
        self.outp.puts(node.s)
        node.v.walkabout(self)
    def visit_binvalue(self, node):
        node.v1.walkabout(self)
        self.outp.puts(node.s)
        node.v2.walkabout(self)
    def visit_value(self, node):
        node.v.walkabout(self)
    def visit_assign(self, node):
        self.outp.puts(node.s)
        self.outp.puts('=')
        node.v.walkabout(self)
    def visit_funccall(self, node):
        self.outp.puts(node.s)
        self.outp.puts('(')
        node.v.walkabout(self)
        self.outp.puts(')')
