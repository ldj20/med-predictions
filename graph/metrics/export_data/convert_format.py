import csv
import math

END_YEAR = 1
LABEL_YEAR = 1
FILENAME = f"./p{END_YEAR}l{LABEL_YEAR}.csv"
start_n2v = 1 + 24*(END_YEAR+1)
end_n2v = start_n2v + END_YEAR

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    n2v_ind = []
    for i in range(start_n2v, end_n2v + 1):
        n2v_ind.append(i)
    with open(FILENAME, newline='\n') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        with open(f"./p{END_YEAR}l{LABEL_YEAR}f.csv", "w") as final:
            i = 0
            for row in reader:
                w = ""
                i += 1
                if (i == 1):
                    for val in row:
                        if val[0:8] == "node2vec":
                            post_year = val[8]
                            for j in range(80):
                                write_val = "node2vec" + post_year + "_" + str(j)
                                w += f'"{write_val}",'
                        else:
                           w += f'"{val}",'
                    w = w[0:len(w)-1]
                    w += "\n"
                    final.write(w)
                    continue
                if i%1000 == 0:
                    print(i)
                w += row[0]
                for ind in range(1, n2v_ind[0]):
                    val = row[ind]
                    num_val = truncate(float(val), 3)
                    w += "," + str(num_val)
                for ind in n2v_ind:
                    ex = row[ind][1:len(row[ind])-1] 
                    arr = ex.split(",")
                    arr = list(map(float, arr))
                    for num_val in arr:
                        w += "," + str(num_val)
                for ind in range(n2v_ind[len(n2v_ind)-1]+1, len(row)):
                    val = row[ind]
                    num_val = truncate(float(val), 3)
                    w += "," + str(num_val)
                w += "\n"
                final.write(w)