package com.prj1;

import java.util.ArrayList;
import java.util.List;

/** LeetCode 241 (B түвшин). Үйлдэл бүрээр хоёр хувааж, хоёр талын бүх хариуг хослуулна. */
public class DifferentWays {

    /** Дахин дуудалтын тоо (хэмжилтэд). */
    public long calls = 0;

    public List<Integer> diffWaysToCompute(String expression) {
        calls++;
        List<Integer> results = new ArrayList<>();
        for (int i = 0; i < expression.length(); i++) {
            char ch = expression.charAt(i);
            if (ch == '+' || ch == '-' || ch == '*') {
                List<Integer> left = diffWaysToCompute(expression.substring(0, i));
                List<Integer> right = diffWaysToCompute(expression.substring(i + 1));
                for (int x : left) {
                    for (int y : right) results.add(apply(x, y, ch));
                }
            }
        }
        if (results.isEmpty()) results.add(Integer.parseInt(expression));
        return results;
    }

    static int apply(int x, int y, char op) {
        return op == '+' ? x + y : op == '-' ? x - y : x * y;
    }
}
