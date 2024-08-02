# Mark 1-8 Computer
My first successful attempt (out of dozens) in making a totally-working computer, in Logisim, that is on par with ones built in 1970s. This computer can do basic arithmetics and logic functions, along with simple if-then algorithms. Not much memory, just 8x256bits of Static RAM.
(Heck, it's not even enough to land a man on the moon!)

Version history  
v1.0  : First working iteration, basic functionalities added, with I/O instruction hardware unbuilt.

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

**Operand Byte H**  
| H<sub>7</sub> | H<sub>6</sub> | H<sub>5</sub> | H<sub>4</sub> | H<sub>3</sub> | H<sub>2</sub> | H<sub>1</sub> | H<sub>0</sub> |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

**Opcode Table, O<sub>7</sub>-O<sub>4</sub>**
| O<sub>6</sub>-O<sub>4</sub> | --> | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **O<sub>7</sub>** | **0** | LDA | STA | MOV | INB | OUT | JMP | JIF | HLT |
| **O<sub>7</sub>** | **1** | ADD | SUB | CMP | AND | OR | XOR | INV | &nbsp; |

**Register Encoding, 2-bit Pair (O<sub>3</sub>..O<sub>2</sub>, O<sub>1</sub>..O<sub>0</sub>)**
| 00 | 01 | 10 | 11 |
| - | - | - | - |
| AC | RX | RY | RZ |

**Flag Register Layout & Encoding, 2-bit Pair (O<sub>3</sub>..O<sub>2</sub>)**
| F<sub>3</sub> | F<sub>2</sub> | F<sub>1</sub> | F<sub>0</sub> |
| - | - | - | - |
| **00** | **01** | **10** | **11** |
| C | A | E | Z |

## Instruction Set Architecture
