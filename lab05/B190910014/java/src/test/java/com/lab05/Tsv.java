package com.lab05;

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
        if (!Files.exists(p)) p = MINE.resolve(name);   // өөрөө зохиосон оролт
        if (!Files.exists(p)) {
            throw new IllegalStateException(
                name + " олдсонгүй (" + SHARED + " эсвэл " + MINE + "). "
                  + "mvn-ийг lab05/<Student-ID>/java/ дотроос ажиллуулж байна уу?");
        }
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

    public static int[] ints(String s) {
        s = s.trim();
        if (s.isEmpty()) return new int[0];
        String[] parts = s.split(",");
        int[] r = new int[parts.length];
        for (int i = 0; i < parts.length; i++) r[i] = Integer.parseInt(parts[i].trim());
        return r;
    }

    public static List<String> strs(String s) {
        s = s.trim();
        if (s.isEmpty()) return List.of();
        return Arrays.asList(s.split(","));
    }

    public static Path writeResults(String language, String[] header,
                                    List<Object[]> data) {
        return writeResults("results", language, header, data);
    }

    public static Path writeResults(String name, String language, String[] header,
                                    List<Object[]> data) {
        try {
            Files.createDirectories(OUT);
            Path p = OUT.resolve(name + "_" + language + ".tsv");
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
