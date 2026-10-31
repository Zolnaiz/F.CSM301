# Лаб №1 — Орчин бэлтгэх

- Оюутны ID: **B190910014**
- Сонгосон хэл: **Python, Java**
- Линукс орчин: **WSL2 (Ubuntu 22.04)**, Windows 11 Home

## 1. Линукс орчин

Windows дээр WSL2-оор Ubuntu-22.04 суулгаж, дараах командуудыг WSL терминалаас ажиллуулав.

### `uname -a`

```text
Linux DESKTOP-RA4LUQ2 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

### `lscpu`

```text
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        39 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               12
On-line CPU(s) list:                  0-11
Vendor ID:                            GenuineIntel
Model name:                           13th Gen Intel(R) Core(TM) i5-1334U
CPU family:                           6
Model:                                186
Thread(s) per core:                   2
Core(s) per socket:                   6
Socket(s):                            1
Stepping:                             3
BogoMIPS:                             4992.00
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid tsc_known_freq pni pclmulqdq vmx ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_vnni vnmi umip waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize flush_l1d arch_capabilities
Virtualization:                       VT-x
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            288 KiB (6 instances)
L1i cache:                            192 KiB (6 instances)
L2 cache:                             7.5 MiB (6 instances)
L3 cache:                             12 MiB (1 instance)
NUMA node(s):                         1
NUMA node0 CPU(s):                    0-11
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Mitigation; Clear Register File
Vulnerability Retbleed:               Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Enhanced / Automatic IBRS; IBPB conditional; RSB filling; PBRSB-eIBRS SW sequence; BHI BHI_DIS_S
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected
```

### `g++ --version`

```text
g++ (Ubuntu 11.4.0-1ubuntu1~22.04.3) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

### `java -version`

```text
openjdk version "17.0.20.1" 2026-08-18
OpenJDK Runtime Environment (build 17.0.20.1+1-1-22.04-Ubuntu)
OpenJDK 64-Bit Server VM (build 17.0.20.1+1-1-22.04-Ubuntu, mixed mode, sharing)
```

### `python3 --version`

```text
Python 3.10.12
```

## 2. Код засварлагч

WSL Ubuntu дээр **Vim 8.2** ашиглаж, `~/.vimrc` файлыг тохируулав. Шаардлагатай багцууд:

| Төрөл | Багц | Товчлол (`<leader>` = Space) |
| ----- | ---- | ---------------------------- |
| Plugin Manager | [vim-plug](https://github.com/junegunn/vim-plug) | `:PlugInstall`, `:PlugUpdate` |
| LSP | [vim-lsp](https://github.com/prabirshrestha/vim-lsp) + [vim-lsp-settings](https://github.com/mattn/vim-lsp-settings), Python-д `python3-pylsp` 1.3.3 | `gd`, `gr`, `K`, `<leader>rn` |
| File Tree | [NERDTree](https://github.com/preservim/nerdtree) | `<leader>e` |
| Finder | [fzf](https://github.com/junegunn/fzf) 0.74.4 + [fzf.vim](https://github.com/junegunn/fzf.vim), ripgrep 13.0.0 | `<leader>p` (`:Files`), `<leader>/` (`:Rg`) |
| Git wrapper | [vim-fugitive](https://github.com/tpope/vim-fugitive) | `<leader>gs` (`:Git`), `<leader>gb` |

Шалгалтын `tsv` файлд tab ашиглах хоёр мөрийг нэмсэн. `vim test_data/fibonacci.tsv`
нээхэд tab нь `>-` хэлбэрээр харагдана.

`~/.vimrc`-ийн гол хэсэг:

```vim
call plug#begin('~/.vim/plugged')
Plug 'preservim/nerdtree'                               " File Tree
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }     " Finder
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-fugitive'                               " Git wrapper
Plug 'prabirshrestha/vim-lsp'                           " LSP
Plug 'mattn/vim-lsp-settings'
call plug#end()

if executable('pylsp')
  autocmd User lsp_setup call lsp#register_server({
        \ 'name': 'pylsp',
        \ 'cmd': {server_info -> ['pylsp']},
        \ 'allowlist': ['python'],
        \ })
endif

autocmd BufRead,BufNewFile *.tsv setlocal noexpandtab
autocmd BufRead,BufNewFile *.tsv setlocal list listchars=tab:>-,trail:~
```

## 3. Даалгаврын сан

Багшийн `batmunkh.d/f.csm301-2627` санг өөрийн GitLab бүртгэл уруу салбарлаж
(<https://gitlab.com/Zolnaiz/f.csm301-2627>), `origin` (өөрийн салбарлалт), `upstream`
(багшийн сан) холболтыг HTTPS-ээр тохируулаад, `main`-аас үүсгэсэн `lab01` салбар дээр ажиллав.

```text
$ git remote -v
origin    https://gitlab.com/Zolnaiz/f.csm301-2627.git (fetch)
upstream  https://gitlab.com/batmunkh.d/f.csm301-2627.git (fetch)
```

## 4. Фибоначчийн тоо

Функц: `python/src/fibonacci.py` (`fibonacci`, `fibonacci_recursive`),
`java/src/main/java/com/lab01/Fibonacci.java` (`fibonacci`, `fibonacciRecursive`).

### (a) Дахин дуудах хувилбар

Тодорхойлолтыг шууд хөрвүүлсэн `fib(n-1) + fib(n-2)` хувилбар n = 0..10 тохиолдлыг
амархан давна (`test_fibonacci_recursive_small`, `fibonacciRecursiveSmall`).

Гэвч дуудалтын мод нь n-ийн хувьд экспоненциалаар өсдөг. Дуудалтын тоо
C(n) = C(n−1) + C(n−2) + 1 = 2F(n+1) − 1 буюу Θ(φⁿ), φ ≈ 1.618.
Хэмжилт (Windows 11, i5-1334U):

| n  | Python (рекурс) | Java (рекурс) |
| -- | --------------: | ------------: |
| 20 |          1.1 ms |        1.1 ms |
| 25 |         12.9 ms |        0.2 ms |
| 30 |        108.1 ms |        2.6 ms |
| 35 |         1214 ms |       29.4 ms |
| 40 |               — |      330.5 ms |
| 42 |               — |      875.9 ms |

n нэгээр өсөхөд хугацаа ойролцоогоор φ ≈ 1.6 дахин нэмэгдэж байна. Python дээр
n ≈ 38-аас эхлэн нэг тохиолдол шалгалтын 5 секундын хязгаараас хэтэрнэ
(n = 45 үед ойролцоогоор 1214 ms · φ¹⁰ ≈ 150 с).

### (b) Бүх мөрийг давуулах

Өмнөх хоёр утгыг санаж давталтаар явбал Θ(n) хугацаа, Θ(1) санах ой зарцуулна:

```python
prev, curr = 0, 1
for _ in range(n):
    prev, curr = curr, prev + curr
return prev
```

`fibonacci.tsv`-ийн 46 мөр (n = 0..45) хоёр хэл дээр бүгд давсан. n = 45 үед
Python 5.9 µs, Java 27.6 µs (JIT халаагүй эхний дуудалт).

### (c) Буруу оролт

n < 0 үед Python `ValueError`, Java `IllegalArgumentException` шиднэ.
`fibonacci_invalid.tsv`-ийн n = −1, −45 тохиолдлуудаар шалгав (`test_fibonacci_invalid`,
`fibonacciInvalid`).

### (d) n = 46, 47

`fibonacci.tsv`-ийн хуулбар болох `test_data/fibonacci_my.tsv` файлд n = 46, 47 мөрийг
нэмж, тусдаа шалгалтаар (`test_fibonacci_my`, `fibonacciMy`) шалгав.

| n  | Хүлээгдэх утга | Python `int` | Java `long` | Java `int` (харьцуулахад) |
| -- | -------------: | -----------: | ----------: | ------------------------: |
| 46 |     1836311903 |   1836311903 |  1836311903 |                1836311903 |
| 47 |     2971215073 |   2971215073 |  2971215073 |           **−1323752223** |

- Python-ы `int` дурын нарийвчлалтай тул халихгүй.
- Java-ийн `int` нь 32 битийн тэмдэгтэй, хамгийн их утга нь 2³¹ − 1 = 2147483647.
  F(46) багтах ч F(47) = 2971215073 > 2³¹ − 1 тул халиж
  2971215073 − 2³² = −1323752223 болно. Иймд загварт өгсөн `long` (64 бит,
  ≈ 9.22·10¹⁸) төрлийг хадгалав. `long` нь F(92) хүртэл багтана.

## 5. Анаграммын шалгалтын өгөгдөл

`anagrams_01.tsv`-ийн 5 мөрөөр өгөгдсөн функцийг ажиллуулж бүтцийг ойлгосны дараа
`test_data/anagrams_my.tsv` файлд 12 шинэ тохиолдол нэмэв (загварт байсан 1 мөр хамт).

| # | Оролт | Шалгаж буй зүйл |
| - | ----- | --------------- |
| 1 | `listen,silent,enlist,google,gooegl` | 3 ба 2 гишүүнтэй хоёр бүлэг |
| 2 | `Aa,aA,aa` | Том, жижиг үсэг ялгаатай: `aa` бүлэгт орохгүй |
| 3 | `abc,def,ghi` | Анаграмм огт байхгүй — хоосон хариу |
| 4 | `x` | Ганц үг — хоосон хариу |
| 5 | `aab,aba,baa,abb,bab` | Ижил үсгүүдтэй ч давтамж нь өөр бүлгүүд |
| 6 | `a,b,a,c,b` | Нэг үсэгтэй үгс, ганц `c` хасагдана |
| 7 | `abc,abcd,dcba,cba` | Урт нь өөр үгс өөр бүлэгт орно |
| 8 | `Tea,Eat,ate,eta` | Том үсэгтэй `Tea`, `Eat` нь `ate`-тэй анаграмм биш |
| 9 | `stop,pots,tops,spot,opts,post` | Нэг том бүлэг (6 гишүүн) |
| 10 | `ab,ba,ab` | Давхардсан үг бүлэгт хоёр удаа үлдэнэ |
| 11 | `123,321,213,12` | Цифр тэмдэгт |
| 12 | `нар,ран,бат,тба,нар` | Кирилл (UTF-8) үсэг |

Хоёр хэл дээр бүх тохиолдол давсан.

## 6. Шалгалтын үр дүн

| Хэл | Команд | Үр дүн |
| --- | ------ | ------ |
| Python | `cd python && .venv/bin/pytest -v` | 125 passed |
| Java | `cd java && mvn test` | Tests run: 125, Failures: 0 |
