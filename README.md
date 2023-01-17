# CSA Lab 3

- Выполнил: Богатов Александр
- Группа: Р33302
- ```asm | acc | harv | mc | tick | struct | stream | port | prob2```

## Язык программирования

```
<program> ::= <section_list> <EOF>
<section_list> ::= <section> <section_list> | <section>
<section> ::= "." <identifier> <EOL> <line_list>
<line_list> ::= <line> <line_list> | <line>
<line> ::= <line_instruction> <EOL> | <EOL>
<line_instruction> ::= <label_decl> | <instruction> | <variable_declaration>
<variable_declaration> ::= <identifier> <type> <letter_or_number_list>
<label_decl> ::= <label> ":"
<label> ::= <identifier>
<identifier> ::= <letter> | <letter> <letter_or_number_list>

<instruction> ::= <no_arg_instr> | <one_arg_instr>
<no_arg_instr> ::= <no_arg_op>
<one_arg_instr> ::= <one_arg_op> <operand>
<operand> ::= <relative_operand> | <abs_operand>
<abs_operand> ::= <label> | <immediate>
<relative_operand> ::= "[" <label> "]"
<immediate> ::= <int_lit> | <char_lit>

<int_lit> ::= <number_list> | "-" <number_list>
<number_list> ::= <number> <number_list> | <number>
<char_lit> ::= "'" <letter> "'" | "'" <number> "'"

<letter_or_number_list> ::= <letter_or_number> | <letter_or_number> <letter_or_number_list>
<letter_or_number> ::= <letter> | <number>

<letter> ::= [a-z] | [A-Z]
<number> ::= [0-9]

<EOF> ::= "1A"
<EOL> ::= "\n"

<type> ::= "STRING" | "NUMERIC" | "CHAR"
<no_arg_op> ::= "inc" | "sh" | "in" | "out" | "hlt"
<one_arg_op> ::= "add" | "ld" | "cmp" | "je" | "jg" | "jmp" | "wr"
```

- В коде asm могут присутствовать 2 секции: .data и .text.

Вне секций объявление данных или код запрещен.
Секция data идет раньше секции text

- Поддерживаются метки. Для обозначения строки как метки, в строке должно быть одно слово и символ ":" в конце.
- Строки ".data:" и ".text:" объявляют секции. На них нельзя ссылаться из кода.

- ac/AC - ссылка на регистр acc - аккумулятор, например:
```
ld [ac]
```

- Данные бывают трех типов: STRING (нуль-терминированные строки), CHAR (символы), NUM (целые числа). Тип должен быть указан после названия переменной. Символы и строки должны быть заключены в двойные кавычки. При записи в память строки разбиваются посимвольно.
- Точка входа в программу - первая инструкция после метки .text

## Организация памяти

- Машинное слово - 32 бита.
- Используется гарвардская архитектура - команды и данные лежат в разных блоках памяти.

### Работа с командами

Регистры:
- acc - аккумулятор
- ip - instruction pointer
- addr - регистр адреса
- z - флаг zero для результата АЛУ
- n - флаг negative для результата АЛУ
- mc_pointer - указатель в память микрокоманд

### Набор инструкций

Все инструкции, требующие участие двух аргументов, берут значение из аккумулятора и из заданной в качестве аргумента ячейки памяти, а после выполняют с ними действия.
Операции, выполняемые по тактам:
- Выборка инструкции (0 такт)
- Выборка адреса (если требуется) и исполнение команды (1 / 1 и 2 такт)
- Изменение ip (2 / 3 такт)

| Синтаксис               | Такты                | Комментарий                                                        |
|:------------------------|:------------------|:-------------------------------------------------------------------| 
| CMP <label>             | 4    | Выполняется как вычитание без записи в acc                         |
| SH                      | 4 | Битовый сдвиг acc                                                  |
| JE <label>              | 3 | Если z=1, ip меняется на адресную часть JE                         |
| JG <label>              | 3 | Если n=1, ip меняется на адресную часть JG                         |
| LD <[ac]/[label]/label> | 3/4 | Адрес операнда или сам операнд записывается в acc                  |
| WR <label>              | 4 | Значение из acc записывается в память                              |
| INC                     | 3 | Значение acc ++                                                    |
| JMP <label>             | 3 | ip меняется на адресную часть JMP                                  |
| ADD <label>             | 4 | Значение acc  += операнд из памяти                                 |
| HLT                     | 3 | Останов                                                            |
| IN                      | 4 | Чтение с устроства ввода  |
| OUT                     | 4 | Запись в устройство вывода |

### Кодирование инструкций

- Код записывается в JSON-файл.

- В этом же списке находятся данные (они лежат перед командами)

- Перед запуском симуляции данные отделяются от кода для симуляции Гарвардской архитектуры

### Память микрокоманд

- Память микрокоманд представляет собой циклическую программу

- Цикл выборки и исполнения инструкций будет продолжаться до тех пор, пока не произойдет ошибка или пока не будет вызвана команда HLT.

| Микрокоманды                                                               | Комментарий |
|:---------------------------------------------------------------------------|:------------------|
| ALU_RIGHT_MUX_ZERO/ALU_RIGHT_MUX_MEM                                       | Сигнал к мультиплексору правого входа АЛУ |
| ALU_LEFT_MUX_ZERO/ALU_LEFT_MUX_ACC                                         | Сигнал к мультиплексору левого входа АЛУ | 
| ALU_SUB/ALU_ADD/ALU_INC/ALU_SH                                             | Сигнал выбора операции АЛУ | 
| ACC_MUX_ALU/ACC_MUX_MEM/ACC_MUX_INPUT                                      | Сигнал к мультиплексору АСС |
| ACC_WRITE                                                                  | Сигнал записи АСС в память | 
| IP_MUX_INC/IP_MUX_INSTR_ADDR_PART                                          | Сигнал к мультиплексору IP | 
| ADDR_MUX_INSTR_ADDR_PART/ADDR_MUX_ACC                                      | Сигнал к мультиплексору ADDR | 
| ACC_LATCH/IP_LATCH/ADDR_LATCH                                              | Сигнал фиксации значений в регистрах | 
| N_SET_GOTO/Z_SET_GOTO/GOTO/CMP_INSTR_NOT_EQ_GOTO/CMP_INSTR_ARG_NOT_EQ_GOTO | Команды перехода в памяти микрокоманд |
| STOP/DECODING_ERR                                                          | Команды останова и ошибки декодирования инструкций |

## Транслятор

- Осуществляется трансляция "на лету": при наличии команд, ссылающихся на еще не определенную метку, эта метка добавляется в словарь зависимостей. Она будет удалена оттуда, как только встретится в коде. Пустой словарь зависимостей - один из признаков успешного завершения трансляции.

Каждая строка в исходном файле может быть:
- пустой (игнорируется)
- меткой
- объявлением секции (особой меткой)
- командой
- объявлением переменной

## Модель процессора

![Scheme](CSA3.png)

Особенности работы модели:

- Для журнала состояний процессора используется стандартный модуль logging.
- Количество инструкций для моделирования ограничено hardcoded константой.
- Остановка моделирования осуществляется при помощи исключения:
    + StopIteration -- если выполнена инструкция halt.
- Управление симуляцией реализовано в функции simulate.

## Апробация

### Пример работы транслятора:

- Исходный код:
```
.data:
max NUMERIC 4000000
b NUMERIC 1
c NUMERIC 2
d NUMERIC 0
sum NUMERIC 0
zero NUMERIC 0
.text:
loop:
ld [c]
cmp max
jg print_result
ld [sum]
add c
wr sum
cmp max
jg print_result
ld [c]
sh
add b
wr d
ld [d]
add c
add b
wr c
ld [zero]
add d
wr b
jmp loop
print_result:
out
hlt
```
- Результат:
```
[
    4000000,
    1,
    2,
    0,
    0,
    0,
    {
        "opcode": "LD_REL",
        "args": [
            2
        ]
    },
    {
        "opcode": "CMP",
        "args": [
            0
        ]
    },
    {
        "opcode": "JG",
        "args": [
            20
        ]
    },
    {
        "opcode": "LD_REL",
        "args": [
            4
        ]
    },
    {
        "opcode": "ADD",
        "args": [
            2
        ]
    },
    {
        "opcode": "WR",
        "args": [
            4
        ]
    },
    {
        "opcode": "CMP",
        "args": [
            0
        ]
    },
    {
        "opcode": "JG",
        "args": [
            20
        ]
    },
    {
        "opcode": "LD_REL",
        "args": [
            2
        ]
    },
    {
        "opcode": "SH",
        "args": [
            0
        ]
    },
    {
        "opcode": "ADD",
        "args": [
            1
        ]
    },
    {
        "opcode": "WR",
        "args": [
            3
        ]
    },
    {
        "opcode": "LD_REL",
        "args": [
            3
        ]
    },
    {
        "opcode": "ADD",
        "args": [
            2
        ]
    },
    {
        "opcode": "ADD",
        "args": [
            1
        ]
    },
    {
        "opcode": "WR",
        "args": [
            2
        ]
    },
    {
        "opcode": "LD_REL",
        "args": [
            5
        ]
    },
    {
        "opcode": "ADD",
        "args": [
            3
        ]
    },
    {
        "opcode": "WR",
        "args": [
            1
        ]
    },
    {
        "opcode": "JMP",
        "args": [
            0
        ]
    },
    {
        "opcode": "OUT",
        "args": [
            -1
        ]
    },
    {
        "opcode": "HLT",
        "args": []
    }
]
```

### Пример трассировки симуляции
```
DEBUG:root:{TICK: 1, ADDR: 0, IP: 0, ACC: 0, Z: 0, N: 0} IN -1
DEBUG:root:{TICK: 2, ADDR: 0, IP: 0, ACC: M, Z: 0, N: 0} IN -1
DEBUG:root:{TICK: 3, ADDR: 0, IP: 1, ACC: M, Z: 0, N: 0} IN -1
DEBUG:root:{TICK: 4, ADDR: 0, IP: 1, ACC: M, Z: 0, N: 0} CMP 0
DEBUG:root:{TICK: 5, ADDR: 0, IP: 1, ACC: M, Z: 0, N: 0} CMP 0
DEBUG:root:{TICK: 6, ADDR: 0, IP: 1, ACC: M, Z: 0, N: 1} CMP 0
DEBUG:root:{TICK: 7, ADDR: 0, IP: 2, ACC: M, Z: 0, N: 1} CMP 0
DEBUG:root:{TICK: 8, ADDR: 0, IP: 2, ACC: M, Z: 0, N: 1} JE 5
DEBUG:root:{TICK: 9, ADDR: 0, IP: 2, ACC: M, Z: 0, N: 1} JE 5
DEBUG:root:{TICK: 10, ADDR: 0, IP: 3, ACC: M, Z: 0, N: 1} JE 5
...
DEBUG:root:{TICK: 164, ADDR: 0, IP: 5, ACC: , Z: 1, N: 0} HLT no arg
DEBUG:root:{TICK: 165, ADDR: 0, IP: 5, ACC: , Z: 1, N: 0} HLT no arg
DEBUG:root:{TICK: 166, ADDR: 0, IP: 5, ACC: , Z: 1, N: 0} HLT no arg
DEBUG:root:Iteration stopped by HLT
```

Папки с...
- [Исходниками](https://gitlab.se.ifmo.ru/albogatov/csa-lab-3/-/tree/master/asm_src)
- [Результатами работы транслятора](https://gitlab.se.ifmo.ru/albogatov/csa-lab-3/-/tree/master/code)
- [Входными данными для симуляции](https://gitlab.se.ifmo.ru/albogatov/csa-lab-3/-/tree/master/io)

| ФИО            | алг.  | LoC (в строках) | code байт | code инстр | инстр. | такт. | вариант |
|:---------------|:------|:----------------| :---|:-----------|:-------|:------| :---| 
| Богатов А.С.   | hello | 18              | -| 26         | 110    | 398   | asm | 
| Богатов А.С.  | cat   | 11              | -| 7          | 49     | 166   | asm | 
| Богатов А.С.  | prob2 | 32              | -| 28         | 210     | 807   | asm | 


