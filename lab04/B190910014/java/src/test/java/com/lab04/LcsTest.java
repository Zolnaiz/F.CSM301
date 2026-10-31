package com.lab04;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.*;

class LcsTest {

    @Test
    void length() {
        for (Map<String, String> r : Tsv.rows("lcs_01.tsv")) {
            assertEquals(Integer.parseInt(r.get("length")),
                    Lcs.length(r.get("X"), r.get("Y")), r.get("id"));
        }
    }

    private record Split(List<String> a, List<String> b, int common) {}

    private static Split split(List<String> diffLines) {
        List<String> a = new ArrayList<>();
        List<String> b = new ArrayList<>();
        int common = 0;
        for (String line : diffLines) {
            assertFalse(line.isEmpty(), "хоосон мөр буцаасан байж болохгүй");
            char sym = line.charAt(0);
            String text = line.substring(1);
            switch (sym) {
                case ' ' -> {
                    a.add(text);
                    b.add(text);
                    common++;
                }
                case '-' -> a.add(text);
                case '+' -> b.add(text);
                default -> fail("мэдэгдэхгүй тэмдэгт: " + line);
            }
        }
        return new Split(a, b, common);
    }

    @Test
    void reconstructsBothSidesAndCommonCount() {
        for (Map<String, String> r : Tsv.rows("diff_01.tsv")) {
            List<String> aIn = Tsv.strs(r.get("A"));
            List<String> bIn = Tsv.strs(r.get("B"));
            Split s = split(Lcs.diff(aIn, bIn));
            assertEquals(aIn, s.a(), r.get("id"));
            assertEquals(bIn, s.b(), r.get("id"));
            assertEquals(Integer.parseInt(r.get("common")), s.common(), r.get("id"));
        }
    }

    @Test
    void realDocumentRevision() throws IOException {
        List<String> before = Files.readAllLines(Tsv.SHARED.resolve("before.txt"), StandardCharsets.UTF_8);
        List<String> after = Files.readAllLines(Tsv.SHARED.resolve("after.txt"), StandardCharsets.UTF_8);
        Split s = split(Lcs.diff(before, after));
        assertEquals(before, s.a());
        assertEquals(after, s.b());
        assertEquals(6, s.common());
    }
}
