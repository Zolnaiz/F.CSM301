package com.lab04;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.regex.*;
import org.junit.jupiter.api.*;

class MatrixChainTest {

    private static final Pattern TOKEN = Pattern.compile("A(\\d+)|[()]");

    private static final class Cursor {
        final String s;
        int pos = 0;

        Cursor(String s) {
            this.s = s;
        }
    }

    private record Dims(int rows, int cols, long cost) {}

    private static Dims parse(Cursor c, int[] p) {
        Matcher m = TOKEN.matcher(c.s);
        assertTrue(m.find(c.pos) && m.start() == c.pos, () -> "буруу тэмдэгт: " + c.s.substring(c.pos));
        if (m.group(1) != null) {
            int i = Integer.parseInt(m.group(1));
            c.pos = m.end();
            return new Dims(p[i - 1], p[i], 0);
        }
        assertEquals('(', c.s.charAt(c.pos), c.s);
        c.pos++;
        Dims left = parse(c, p);
        Dims right = parse(c, p);
        assertTrue(c.pos < c.s.length() && c.s.charAt(c.pos) == ')', c.s);
        c.pos++;
        assertEquals(left.cols(), right.rows(), () -> "хэмжээс таарахгүй: " + c.s);
        long cost = left.cost() + right.cost() + (long) left.rows() * left.cols() * right.cols();
        return new Dims(left.rows(), right.cols(), cost);
    }

    private static long evalCost(String parens, int[] p) {
        Cursor c = new Cursor(parens);
        Dims d = parse(c, p);
        assertEquals(c.s.length(), c.pos, () -> "ашиглагдаагүй тэмдэгт үлдсэн: " + c.s);
        return d.cost();
    }

    @Test
    void orderIsAValidOptimalParenthesization() {
        for (Map<String, String> r : Tsv.rows("matrix_chain_01.tsv")) {
            int[] p = Tsv.ints(r.get("p"));
            long expected = Long.parseLong(r.get("min_mults"));
            MatrixChain.Result res = MatrixChain.order(p);
            assertEquals(expected, res.minMults(), r.get("id"));
            assertEquals(expected, evalCost(res.parens(), p), r.get("id"));
        }
    }
}
