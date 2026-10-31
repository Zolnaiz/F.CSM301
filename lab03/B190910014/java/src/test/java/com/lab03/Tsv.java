package com.lab03;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public final class Tsv {

    public static final Path STUDENT_DIR =
            Paths.get("..").toAbsolutePath().normalize();
    public static final Path LAB_DIR = STUDENT_DIR.getParent();

    public static final Path SHARED = LAB_DIR.resolve("test_data");
    public static final Path MINE = STUDENT_DIR.resolve("test_data");
    public static final Path OUT = STUDENT_DIR.resolve("out");

    public static List<Map<String, String>> rows(String name) {
        Path p = SHARED.resolve(name);
        if (!Files.exists(p)) p = MINE.resolve(name);
        try {
            List<String> lines = Files.readAllLines(p, StandardCharsets.UTF_8);
            String[] head = lines.get(0).split("\t", -1);
            List<Map<String, String>> out = new ArrayList<>();
            for (int i = 1; i < lines.size(); i++) {
                if (lines.get(i).isEmpty()) continue;
                String[] f = lines.get(i).split("\t", -1);
                Map<String, String> m = new LinkedHashMap<>();
                for (int j = 0; j < head.length; j++) {
                    m.put(head[j], j < f.length ? f[j] : "");
                }
                out.add(m);
            }
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    /** "1,2,3" -> {1, 2, 3} */
    public static long[] vector(String s) {
        String[] parts = s.trim().split(",");
        long[] r = new long[parts.length];
        for (int i = 0; i < parts.length; i++) r[i] = Long.parseLong(parts[i].trim());
        return r;
    }

    /** "1,2;3,4" -> {{1, 2}, {3, 4}} */
    public static long[][] matrix(String s) {
        String[] rows = s.trim().split(";");
        long[][] m = new long[rows.length][];
        for (int i = 0; i < rows.length; i++) m[i] = vector(rows[i]);
        return m;
    }

    public static Path writeResults(String language, String[] header, List<Object[]> data) {
        try {
            Files.createDirectories(OUT);
            Path p = OUT.resolve("results_" + language + ".tsv");
            StringBuilder sb = new StringBuilder(String.join("\t", header)).append('\n');
            for (Object[] r : data) {
                for (int i = 0; i < r.length; i++) {
                    if (i > 0) sb.append('\t');
                    sb.append(r[i]);
                }
                sb.append('\n');
            }
            Files.writeString(p, sb.toString(), StandardCharsets.UTF_8);
            return p;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private Tsv() {}
}
