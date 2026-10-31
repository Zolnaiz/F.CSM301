package com.lab01;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Anagrams {

  public static List<List<String>> findAnagrams(List<String> dictionary) {
    Map<String, List<String>> sortedStringToAnagrams = new HashMap<>();
    for (String s : dictionary) {
      String sortedStr = Stream.of(s.split("")).sorted().collect(Collectors.joining());
      sortedStringToAnagrams.putIfAbsent(sortedStr, new ArrayList<String>());
      sortedStringToAnagrams.get(sortedStr).add(s);
    }
    return sortedStringToAnagrams.values()
        .stream()
        .filter(group -> group.size() >= 2)
        .collect(Collectors.toList());
  }
}
