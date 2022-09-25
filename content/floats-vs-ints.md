+++
title = "Floating-points All the Way Down"
date = 2022-09-23
description = ""
+++

## Floating-point representation

Floating-point numbers are stored in a way that resembles scientific notation. It stores two parts: a decimal number between 0 and 1 (called the *mantissa*) and an exponent, along with a bit used to represent whether it is a positive or negative number. Normal integers are stored in simpler format without exponents, and always represent a whole number.

There two main two types of floating-point numbers: the [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) `single` (binary32) and `double` (binary64) precision floating-point numbers. Other, less popular, formats for storing decimal numbers exist but for the rest of this article you should assume either `single` or `double` when I mention a floating-point number.

If you use JavaScript you're actually using 64bit floating point numbers - or `double`s for those familiar with C or Java.

> Well that's not entirely true - there are some internal optimizations that can represent some numbers as integers, but you should just assume all numbers in JavaScript are represented as `double`s (with the exception of explicitly using [`BigInt`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt)s, in which case you already know you're using integers). For more on JS optimization I recommend reading the [V8 Blog](https://v8.dev/blog)

## Accuracy

Perhaps the most overlooked aspect of floating-point numbers is their accuracy. Take the example of adding `0.1 + 0.2` from [The Floating-Point Guide](https://floating-point-gui.de/errors/comparison/). If you tried this in JavaScript or Python you would *not* get the value `0.3` but instead something like `0.30000000000000004`. However, `0.15 + 0.15` will work and returns `0.3`.  The floating-point formats have limited precision so there will often be some kind of *rounding error*.

A common pitfall is checking equality of two floating-point numbers where one or both are the result of computation. The following returns `false`:

```javascript
0.1 + 0.2 == 0.3  // false
```

Performing computation on floating-point numbers has the potential to create different results, depending on what operations are performed and in what order. Each floating-point operation could potentially create *rounding errors* when the actual computed number would require greater precision than can actually fit into the data type.

### Epsilon

To avoid issues caused by numbers being off by these very small amounts, a margin of error can be used that represents a very small value. This is referred to as epsilon ([Machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)), and represents the difference between 1.0 and the next largest number that can be represented in the data type (so something similar to 1.000001 but even smaller). Instead of checking two floating-point numbers for equality instead subtract them and compare that difference against epsilon. It should be noted that you may have to use a value greater than epsilon. For example, I have had to use `epsilon * 3.0` in some of my code to get correct results, but that is still a very small number.

#### Epsilon in Python

Epsilon in Python is represented by `sys.float_info.epsilon`

```python
import sys
a = 0.15 + 0.15
b = 0.1 + 0.2

print(f'{a=} {b=}') # a=0.3 b=0.30000000000000004

print(a == b)
# false

print(abs(a - b) < sys.float_info.epsilon)
# true
```

#### Epsilon in JavaScript

Epsilon in JavaScript is represented by `Number.EPSILON`

```javascript
const a = 0.15 + 0.15;
const b = 0.1 + 0.2;

console.log(`a=${a} b=${b}`)
// a=0.3 b=0.30000000000000004

console.log(a == b);
// false

console.log(Math.abs(a-b) < Number.EPSILON);
// true
```

Notice the value of `b`, which returns 0.30000000000000004.

## Special values

Floating-point numbers can also represent special values like infinity and negative infinity. With integer math dividing by 0 will just raise an exception, however with floating-point math you will instead get `infinity`. Trying `-10.0 / 0.0` in Python will actually still raise an exception, however in many other languages, like JavaScript, it will happily return `-infinity`. Notice how it's *negative* infinity, because we divided by -10.

Likewise, trying `0.0 / 0.0` will produce another special value called `NaN` which stands for "Not a Number". These can propagate through math operations, which may cause some confusion to programmers who expect invalid operations to just throw an error. So `0.0 / 0.0 + 2.0 + 10.0` will still give us a `NaN` - the 0 divided by 0 "poisoned" it so that all following operations in the computation also produce `NaN`. There are also two types of `NaN`, but I won't get into that here.

Here are some more examples of surprising behavior:

```javascript
console.log(0.0/0.0 == 0.0/0.0);
// false: NaN does NOT equal Nan

console.log(-0.0 == 0.0);
// true: zero is zero regardless of the sign

console.log(Number.MAX_SAFE_INTEGER - 1.1)
// 9007199254740990

```

## Performance

Performance is, IMHO, the least important aspect of floating-point numbers for most programmers. However, if you don't need decimal numbers you can get a small performance benefit by using integers. It should be noted that this rarely makes a significant difference - most instructions happen very fast regardless of whether they use integer or floating-point numbers.

Most modern processors have a [Floating-point unit](https://en.wikipedia.org/wiki/Floating-point_unit) that is dedicated to working with floating-point numbers. In modern processors those floating-point processing units are fairly efficient, but there is still a performance penalty.

Even casting a floating-point number to an integer number can affect performance. This is especially important when dealing with pointer arithmetic and array indexes, which require integers.

### Vector Instructions

To get around performance issues processors introduced special, low-level, vector instruction sets, like SSE and AVX, that are able to perform operations on multiple numbers at once. This is actually a type of parallel programming.

For example, if you wanted to multiple the following vectors of numbers together, you would normally loop from <a href="https://en.wikipedia.org/wiki/Interval_(mathematics)#Terminology"><dfn title="A range including 0 but excluding 4">[0..4)</dfn></a> and multiply corresponding elements, like:

```javascript
let a = [10, 20, 30, 40];
let b = [4, 3, 2, 1];
let result = [];

for(i in [0,1,2,3]) {
  result[i] = a[i] * b[i];
}

console.log(result); 
// [40, 60, 60, 40]
```

Instead, vector instructions would simultaneously multiply the first number from each array, then the second number from each, and so on. Vector instructions work on specific sizes, often 128 or 256 bits of data. If you are using 256bit vector types, you can store either 8 `single`s or 4 `double`s. The following pseudo-code represents what is happening better:

```c
[10, 20, 30, 40] * [4, 3, 2, 1]
```

There is no need for an explicit loop, it just takes each element and multiplies them together. Each multiplication is happening at the same time, within the same processor instruction. This is very helpful for improving performance, the processor doesn't need to [fetch, decode, and execute](https://en.wikipedia.org/wiki/Instruction_cycle) the instructions for each multiplication operation. The downsides are that the processor has to support these instructions, and explicitly using them often require a low-level language.

### SMT

[Simultaneous multithreading](https://en.wikipedia.org/wiki/Simultaneous_multithreading), or better known as Hyper-threading in Intel processors, is a technique used to improve performance under heavy multi-threaded loads. For example, SMT can take advantage of the fact that modern processors have a separate processing unit for integer operations versus floating-point operations. Each x86-64 processor core (logical processor) would be able to perform one operation on its [Arithmetic logic unit](https://en.wikipedia.org/wiki/Arithmetic_logic_unit) (ALU) and another on its [Floating-point unit](https://en.wikipedia.org/wiki/Floating-point_unit) (FPU) at the same time.

So in a strange way it is possible to *increase* performance by using floating-point numbers. By using multiple threads, each one performing either floating-point or integer math, you could better saturate the processor. Most programs won't benefit from this much, but computationally intensive programs may see a noticeable performance boost.

## Alternatives

Other types do exist besides the IEEE binary floating-point formats. For most applications they will work fine, however it is important to know when to reach for another data type. 

Some languages support decimal floating-point types like [`decimal32`](https://en.wikipedia.org/wiki/Decimal32_floating-point_format) and [`decimal64`](https://en.wikipedia.org/wiki/Decimal64_floating-point_format). The decimal floating-point numbers are more accurate this way and are a better fit when precision is required, like for financial applications.

There are also libraries that have arbitrary precision, like [`mpmath`](https://mpmath.org/) for Python, which can store extremely precise numbers at the expense of memory and computation speed.  These are often used a last resort when other standard types are not precise enough.
