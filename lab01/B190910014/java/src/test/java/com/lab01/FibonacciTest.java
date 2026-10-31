package com.lab01;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvFileSource;
import org.junit.jupiter.params.provider.MethodSource;

class FibonacciTest {

  @ParameterizedTest(name = "F({0}) = {1}")
  @CsvFileSource(files = "../test_data/fibonacci.tsv",
                 delimiter = '\t',
                 numLinesToSkip = 1)
  @Timeout(value = 5, unit = TimeUnit.SECONDS)
  void fibonacci(int n, long expected) {
    assertEquals(expected, Fibonacci.fibonacci(n));
  }

  /** fibonacci.tsv-ийн n = 0..10 мөрүүд. */
  static Stream<Arguments> smallCases() throws IOException {
    return Files.readAllLines(Path.of("../test_data/fibonacci.tsv")).stream()
        .skip(1)
        .filter(line -> !line.isBlank())
        .map(line -> line.split("\t"))
        .filter(f -> Integer.parseInt(f[0]) <= 10)
        .map(f -> Arguments.of(Integer.parseInt(f[0]), Long.parseLong(f[1].trim())));
  }

  /** (a) алхам: дахин дуудах хувилбар n = 0..10 тохиолдлыг давна. */
  @ParameterizedTest(name = "F({0}) = {1}")
  @MethodSource("smallCases")
  @Timeout(value = 5, unit = TimeUnit.SECONDS)
  void fibonacciRecursiveSmall(int n, long expected) {
    assertEquals(expected, Fibonacci.fibonacciRecursive(n));
  }

  /** (c) алхам: n < 0 үед IllegalArgumentException шидэнэ. */
  @ParameterizedTest(name = "n = {0}: {1}")
  @CsvFileSource(files = "../test_data/fibonacci_invalid.tsv",
                 delimiter = '\t',
                 numLinesToSkip = 1)
  void fibonacciInvalid(int n, String reason) {
    assertThrows(IllegalArgumentException.class, () -> Fibonacci.fibonacci(n));
  }

  /** (d) алхам: хуулбар файлд n = 46, 47 нэмсэн. */
  @ParameterizedTest(name = "F({0}) = {1}")
  @CsvFileSource(files = "../test_data/fibonacci_my.tsv",
                 delimiter = '\t',
                 numLinesToSkip = 1)
  @Timeout(value = 5, unit = TimeUnit.SECONDS)
  void fibonacciMy(int n, long expected) {
    assertEquals(expected, Fibonacci.fibonacci(n));
  }
}
