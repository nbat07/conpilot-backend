import java.util.*;
public class MarksManager {
    // Keep the answer in a colon and semi-colon separated format such as 101:30;102:20
    public static String manageMarks(int records, List<String> inputs) {
        Map<Integer, Integer> a = new HashMap<>();
        List<String[]> lst = new ArrayList<>();
        for (int i = 0; i < records; i++) {
            lst.add(inputs.get(i).split(","));
        }
        for (String[] i : lst) {
            int x = Integer.parseInt(i[0].trim());
            int y = Integer.parseInt(i[i.length - 1].trim());
            if (a.containsKey(x)) {
                a.put(x, a.get(x) + y);
            } else {
                Map<Integer, Integer> b = new HashMap<>();
                b.put(x, y);
                a.putAll(b);
            }
        }
        List<String> L1 = new ArrayList<>();
        for (Map.Entry<Integer, Integer> entry : a.entrySet()) {
            L1.add(String.format("%d:%d", entry.getKey(), entry.getValue()));
        }
        Collections.sort(L1);return String.join(";", L1);
    }
}