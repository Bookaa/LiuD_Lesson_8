# LiuD_Lesson_8
LiuD lesson eight

we already support,

    int i = 22
    int j = 3 + i
    int k
    k = i - j
    print(k)

as syntax:

    option.prefix = GDL01
    states.skip = crlf
    main = stmt*
    stmt := declare_with_value | declare | assign | funccall
    datatype = 'int' | 'long'
    declare = datatype NAME
    declare_with_value = datatype NAME '=' value
    value0 = NUMBER | NAME
    binvalue = value0 ('+' | '-') value0
    value := binvalue | value0
    assign = NAME '=' value
    funccall = NAME '(' value ')'

now, lets support more,

    int i = 22
    int j = 3 + i
    int k
    k = i - j * 3
    print(k)

as syntax:

    option.prefix = GDL01
    states.skip = crlf
    main = stmt*
    stmt := declare_with_value | declare | assign | funccall
    datatype = 'int' | 'long'
    declare = datatype NAME
    declare_with_value = datatype NAME '=' value
    value0 = NUMBER | NAME
    value1 := value0 | enclosed
        enclosed = '(' value ')'
    value2 := signed | value1
        signed = ('-' | '+') value1
    binvalue = value2 (, '**' ('*' '/') ('+' '-') ('>=' '>' '<=' '<' '==' '!=')) value1
    value := binvalue
    assign = NAME '=' value
    funccall = NAME '(' value ')'

add new GDL syntax:

    value = A (, 'op1' 'op2') B

means:

    tem1 = A ('op1' B)*
    tem2 = tem1 ('op2' B)*
    value := tem2 | tem1 | A



