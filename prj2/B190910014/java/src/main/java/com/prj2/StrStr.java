package com.prj2;

/** LeetCode 28. KMP: Θ(n + m) хугацаа, Θ(m) санах ой. String.indexOf/contains ашиглахгүй. */
public class StrStr {

    public int strStr(String haystack, String needle) {
        int m = needle.length();
        if (m == 0) return 0;
        int[] fail = new int[m]; // needle[0..i]-ийн хамгийн урт жинхэнэ угтвар = дагавар
        for (int i = 1, k = 0; i < m; i++) {
            while (k > 0 && needle.charAt(i) != needle.charAt(k)) k = fail[k - 1];
            if (needle.charAt(i) == needle.charAt(k)) k++;
            fail[i] = k;
        }
        for (int i = 0, k = 0; i < haystack.length(); i++) {
            char ch = haystack.charAt(i);
            while (k > 0 && ch != needle.charAt(k)) k = fail[k - 1];
            if (ch == needle.charAt(k) && ++k == m) return i - m + 1;
        }
        return -1;
    }

    /** Харьцуулах: байрлал бүрээс тэмдэгт тэмдэгтээр, O(n·m). */
    public int strStrNaive(String haystack, String needle) {
        int n = haystack.length();
        int m = needle.length();
        for (int start = 0; start + m <= n; start++) {
            int j = 0;
            while (j < m && haystack.charAt(start + j) == needle.charAt(j)) j++;
            if (j == m) return start;
        }
        return -1;
    }
}
