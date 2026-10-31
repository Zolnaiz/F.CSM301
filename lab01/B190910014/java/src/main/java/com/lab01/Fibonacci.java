package com.lab01;

public class Fibonacci {

  /**
   * (a) алхам: тодорхойлолтоор шууд бичсэн хувилбар. Ажиллах хугацаа нь
   * экспоненциал тул зөвхөн бага n-д л хэрэглэгдэнэ.
   */
  public static long fibonacciRecursive(int n) {
    if (n < 0) {
      throw new IllegalArgumentException("n сөрөг байж болохгүй: " + n);
    }
    if (n < 2) {
      return n;
    }
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
  }

  /** F(0) = 0, F(1) = 1 дарааллын n-р гишүүнийг Θ(n) хугацаанд буцаана. */
  public static long fibonacci(int n) {
    if (n < 0) {
      throw new IllegalArgumentException("n сөрөг байж болохгүй: " + n);
    }
    long prev = 0;
    long curr = 1;
    for (int i = 0; i < n; i++) {
      long next = prev + curr;
      prev = curr;
      curr = next;
    }
    return prev;
  }
}
