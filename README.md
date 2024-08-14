# Mark 1-8 Computer
My first successful attempt (out of dozens) in making a totally-working computer, in Logisim, that is on par with ones built in 1970s. This computer can do basic arithmetics and logic functions, along with simple if-then algorithms. Not much memory, just 8x256bits of Static RAM.
(Heck, it's not even enough to land a man on the moon!)

Version history  
v1.0  : First working iteration, basic functionalities added, with I/O instruction hardware unbuilt.

## Circuit Diagram
![Mark1Computer_DieShot](https://github.com/user-attachments/assets/b61b36f0-7143-4722-a092-4e105b5626c1)

## Register Layout

**General-Purpose Registers**
- **AC**  Accumulator, stores result of every math operation  
- **RX**  Register X, index register  
- **RY**  Register Y, index register  
- **RZ**  Register Z, index register

**Memory-Related Registers**
- **PC**  Program counter, points to instructions in RAM  
- **MAR**  Memory address register, stores address to be evaluated in RAM  
- **MDI**  Memory data-in register, stores contents to be inputted to RAM  
- **MDO**  Memory data-out register, stores the outputted contents of RAM

**Processor Registers**
- **IR**  Instruction register, stores currently executed instruction  
- **FLAG**  Flag register, stores the flag and processor statuses after each instruction (4 bits wide)

## Instruction Layout
**Opcode Byte O**  
| O<sub>7</sub> | O<sub>6</sub> | O<sub>5</sub> | O<sub>4</sub> | O<sub>3</sub> | O<sub>2</sub> | O<sub>1</sub> | O<sub>0</sub> |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

**Operand Byte H (Serves as Address Pointer)**  
| H<sub>7</sub> | H<sub>6</sub> | H<sub>5</sub> | H<sub>4</sub> | H<sub>3</sub> | H<sub>2</sub> | H<sub>1</sub> | H<sub>0</sub> |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

**Opcode Table, O<sub>7</sub>-O<sub>4</sub>**
| O<sub>6</sub>-O<sub>4</sub> | --> | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **O<sub>7</sub>** | **0** | LDA | STA | MOV | INB | OUT | JMP | JIF | HLT |
| **O<sub>7</sub>** | **1** | ADD | SUB | CMP | AND | OR | XOR | NOT | &nbsp; |

**Register Encoding, 2-bit Pair (O<sub>3</sub>..O<sub>2</sub>, O<sub>1</sub>..O<sub>0</sub>)**
| 00 | 01 | 10 | 11 |
| - | - | - | - |
| AC | RX | RY | RZ |

**Flag Register Layout & Encoding, 2-bit Pair (O<sub>3</sub>..O<sub>2</sub>)**
| F<sub>3</sub> | F<sub>2</sub> | F<sub>1</sub> | F<sub>0</sub> |
| - | - | - | - |
| **00** | **01** | **10** | **11** |
| C | A | E | Z |

## Instruction Set
All instructions listed below are executed in equal timespan of `ExecTime = 8/ClockFreq`.  
ClockFreq is adjustable via high/low ticks or simulation speed setting.

| **Memory Instruction** | &nbsp; |
| ------------------ | ------ |
| `LDA RR,$XX` | **Load** from address $XX to register RR |
| `STA RR,$XX` | **Store** to  address $XX from register RR |
| `MOV RA,RB` | **Move** from register RA to register RB |
| `INB $XX` | **Input** to address $XX |
| `OUT $XX` | **Output** from address $XX |
| `JMP $XX` | **Jump** to instruction at address $XX |
| `JIF $XX,FF` | **Jump If** flag FF valid to address $XX |
| `HLT` | **Halt** and wait for CPU reset |
| **Math Instruction** | &nbsp; |
| `ADD RA,RB` | **Add** register RA with register RB |
| `SUB RA,RB` | **Subtract** register RA by register RB |
| `CMP RA,RB` | **Compare** register RA with register RB |
| `AND RA,RB` | **Logical AND** register RA with register RB |
| `OR RA,RB` | **Logical OR** register RA with register RB |
| `XOR RA,RB` | **Logical XOR** register RA with register RB |
| `NOT RA` | **Logical NOT** register RA |
| **Data Instruction** | &nbsp; |
| `DATA YY,$XX` | **Place Data** of YY to address $XX |

Some important notes:  
- Register encoding (`RR`, `RA`, `RB`) follows the register encoding rule on **Byte Layout Segment**.  
- Flag encoding (`FF`) follows the flag encoding rule on **Flag Layout & Encoding Segment**.  
- Data `YY` and address `$XX` is displayed in hexadecimal values.
- Per 2-pass assembler v1.0, ```JMP``` and ```JIF``` can only be used with loop labels ```:LOOPLABEL```, further explanation is provided in **Assembly Program Example**.

## Programming The Mark 1-8
1. Download all the files in this directory, especially `Assembler.py`, and place the download in ```C:\``` directory. (Python won't work if it's placed in a directory other than ```C:\``` so beware!)
2. Write your assembly program per the instruction set above, and save it as `*name*.asm`, still in the directory.
3. Open python from command prompt, then type `Python Assembler.py *name*.asm`, then wait until strings of hex numbers with `v3.0` header is printed on the terminal. Copy-paste it into a notepad, then save it as a plain file without any extension, e.g. `*name*`.
4. Open the `Mark1Computer.circ` circuit, then on the RAM, right-click and select "Edit Contents", then select "Open". Select the `*name*` file, then `Ctrl`+`K` to run the clock, and _et voila_!

## Assembly Program Example
This program can be assembled using the ```Assembler_2pass.py``` program, **not** the ```Assembler.py```. 
Per 2-pass assembler v1.1, the assembler can ignore comments.
```
:INITIALIZE
LDA AC,$A0      //AC = 0
LDA RX,$A1      //RX = 0
LDA RY,$A2      //RY = 1
LDA RZ,$A3      //RZ = 224
:ADDITION
STA RX,$A1     //Stores result of RX into respective memory location
OUT $A1        //Outputs RX
ADD RX,RY      //AC = RX + RY
MOV RY,RX      //RX = RY
MOV AC,RY      //RY = AC
CMP RX,RZ      //Compares RX against RZ (fixed value, RZ = 224)
JIF ENDLOOP,A  //Jumps to ENDLOOP if RX > RZ
JMP ADDITION   //Jumps back to ADDITION when previous JIF is not fulfilled
:ENDLOOP
OUT $AF        //Outputs data at $AF (indicates as finish signal)
HLT            //Halts
:VARIABLES
DATA 00,$A0    //A = 0
DATA 00,$A1    //X = 0
DATA 01,$A2    //Y = 1
DATA E0,$A3    //Z = 224
DATA AA,$AF    //Message to be displayed. M = 170
```
