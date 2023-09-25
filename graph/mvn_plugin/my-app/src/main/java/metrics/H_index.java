package metrics;

import java.util.*;

import org.neo4j.procedure.Description;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.UserFunction;

public class H_index {

    @UserFunction
    @Description("metrics.h_index([n1,n2,...]) - returns an h-index given a list of publication citation counts.")
    public double h_index(@Name("citations") List<Double> citations) {
        if (citations == null) {
            return -1.0;
        }
        int n = citations.size();
        double[] arr = new double[n];
        for (int i = 1; i < n+1; i++) {
            arr[i-1] = i;
        }
        citations.sort(Comparator.reverseOrder());
        ArrayList<Double> minima = new ArrayList<Double>();
        for (int i = 0; i < n; i++) {
            minima.add(Math.min(arr[i], citations.get(i)));
        }
        double h_idx = Collections.max(minima);
        return h_idx;
    }
}
/*def h_index_expert(citations):
    n = len(citations)
    array = []
    for i in range(1,n+1):
        array.append(i)
    citations = reverse_sort(citations)
    h_idx = MAX(element_wise_minima(citations, array))
    return h_idxa*/