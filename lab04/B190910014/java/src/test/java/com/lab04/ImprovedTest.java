package com.lab04;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import org.junit.jupiter.api.*;

/** A түвшин: сайжруулсан diff (Myers) ба матрицын цуваа (энгийн дахин дуудалт). */
class ImprovedTest {

    private record Split(List<String> a, List<String> b, int common) {}

    private static Split split(List<String> lines) {
        List<String> a = new ArrayList<>();
        List<String> b = new ArrayList<>();
        int common = 0;
        for (String line : lines) {
            char sym = line.charAt(0);
            String text = line.substring(1);
            if (sym == ' ') { a.add(text); b.add(text); common++; }
            else if (sym == '-') a.add(text);
            else if (sym == '+') b.add(text);
            else fail(line);
        }
        return new Split(a, b, common);
    }

    @Test
    void myersDiff01() {
        for (Map<String, String> r : Tsv.rows("diff_01.tsv")) {
            List<String> aIn = Tsv.strs(r.get("A"));
            List<String> bIn = Tsv.strs(r.get("B"));
            Split s = split(Lcs.diffMyers(aIn, bIn));
            assertEquals(aIn, s.a(), r.get("id"));
            assertEquals(bIn, s.b(), r.get("id"));
            assertEquals(Integer.parseInt(r.get("common")), s.common(), r.get("id"));
        }
    }

    @Test
    void myersRealDocument() throws IOException {
        List<String> before = Files.readAllLines(Tsv.SHARED.resolve("before.txt"), StandardCharsets.UTF_8);
        List<String> after = Files.readAllLines(Tsv.SHARED.resolve("after.txt"), StandardCharsets.UTF_8);
        Split s = split(Lcs.diffMyers(before, after));
        assertEquals(before, s.a());
        assertEquals(after, s.b());
        assertEquals(6, s.common());
    }

    @Test
    void myersCommonEqualsLcsRandom() {
        Random rng = new Random(4);
        for (int t = 0; t < 2000; t++) {
            List<String> a = new ArrayList<>();
            List<String> b = new ArrayList<>();
            int na = rng.nextInt(13);
            int nb = rng.nextInt(13);
            for (int i = 0; i < na; i++) a.add(String.valueOf("abcde".charAt(rng.nextInt(5))));
            for (int i = 0; i < nb; i++) b.add(String.valueOf("abcde".charAt(rng.nextInt(5))));
            Split s = split(Lcs.diffMyers(a, b));
            assertEquals(a, s.a());
            assertEquals(b, s.b());
            assertEquals(Lcs.length(String.join("", a), String.join("", b)), s.common());
        }
    }

    @Test
    void recursiveChainMatches() {
        for (Map<String, String> r : Tsv.rows("matrix_chain_01.tsv")) {
            int[] p = Tsv.ints(r.get("p"));
            MatrixChain.RecursiveResult res = MatrixChain.recursive(p);
            assertEquals(Long.parseLong(r.get("min_mults")), res.minMults(), r.get("id"));
            assertEquals(MatrixChain.order(p).minMults(), res.minMults(), r.get("id"));
            assertEquals((long) Math.pow(3, p.length - 2), res.calls(), r.get("id"));
        }
    }
}
