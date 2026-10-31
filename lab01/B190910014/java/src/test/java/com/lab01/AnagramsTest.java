package com.lab01;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

class AnagramsTest {

  /** "eat,tea" -> [eat, tea]. Хоосон талбар -> []. */
  private static List<String> splitWords(String field) {
    if (field == null || field.isEmpty()) return List.of();
    return Arrays.asList(field.split(",", -1));
  }
 
  /** "eat,tea;tan,nat" -> [[eat, tea], [tan, nat]]. */
  private static List<List<String>> splitGroups(String field) {
    if (field == null || field.isEmpty()) return List.of();
    List<List<String>> out = new ArrayList<>();
    for (String g : field.split(";", -1)) out.add(splitWords(g));
    return out;
  }

  private static List<List<String>> normalize(List<List<String>> groups) {
    List<List<String>> copy = new ArrayList<>();
    for (List<String> g : groups) {
      List<String> inner = new ArrayList<>(g);
      Collections.sort(inner);
      copy.add(inner);
    }
    copy.sort(Comparator.comparing(Object::toString));
    return copy;
  }

  @ParameterizedTest(name = "[{index}] {0}")
  @CsvFileSource(files = "../test_data/anagrams_01.tsv",
                 delimiter = '\t',
                 numLinesToSkip = 1)
  void anagramsLevel1(String words, String expected) {
    assertEquals(normalize(splitGroups(expected)),
                 normalize(Anagrams.findAnagrams(splitWords(words))));
  }

  @ParameterizedTest(name = "[{index}] {0}")
  @CsvFileSource(files = "../test_data/anagrams_my.tsv",
                 delimiter = '\t',
                 numLinesToSkip = 1)
  void anagramsMyCases(String words, String expected) {
    assertEquals(normalize(splitGroups(expected)),
                 normalize(Anagrams.findAnagrams(splitWords(words))));
  }
}
