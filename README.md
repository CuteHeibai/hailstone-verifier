# Hailstone Verifier

冰雹猜想（Collatz 猜想）命令行验证程序。

功能：

- 连续验证多个输入
- 支持 `2^100001-1`、`2**20+3` 和括号表达式
- 使用 `gmpy2` 加速大整数运算
- 大数默认只显示位数，避免终端输出拖慢计算
- 使用 `--full` 参数显示完整数字

运行源码：

```bat
python hailstone.py
```

完整数字显示模式：

```bat
python hailstone.py --full
```

打包后的软件位于 `dist\HailstoneVerifier.exe`。
