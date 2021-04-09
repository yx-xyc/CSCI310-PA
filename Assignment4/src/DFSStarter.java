package src;
import java.util.Scanner; 
import java.util.ArrayList;
import java.io.*;

// Data structure for a node in a linked list
class Item {
    int data;
    Item next;
 
    Item(int data, Item next) {
       this.data = data;
       this.next = next;
      }
   }
   // Data structure for representing a graph
   class Graph {
      int n;  // # of nodes in the graph
      
      Item[] A; 
      // For u in [0..n), A[u] is the adjecency list for u
      
      Graph(int n) {
         // initialize a graph with n vertices and no edges
         this.n = n;
         A = new Item[n];
      }
      
    void addEdge(int u, int v) {
       // add an edge u -> v to the graph
       A[u] = new Item(v, A[u]);
    }

    void printGraph(){
       System.out.println("Length: "+A.length+"\n");
       for (int i=1; i<n;i++){
          if (A[i]!=null){
             System.out.println("Header: "+ i);
             System.out.print("\tEdges: "+ A[i].data);
             Item node = A[i].next;
             while (node!=null){
                System.out.print(", "+ node.data);
                node = node.next;
            }
             System.out.println();
         }
       }
    }
 }
 // Data structure holding data computed by DFS
class DFSInfo {
    
    // node colors
    static final int WHITE = 0;
    static final int GRAY  = 1;
    static final int BLACK = 2;
 
    int[] color;  // variable storing the color
                  // of each node during DFS
                  // (WHITE, GRAY, or BLACK) -> (1,2,3)
 
    int[] parent; // variable storing the parent 
                  // of each node in the DFS forest
 
    int d[];      // variable storing the discovery time 
                  // of each node in the DFS forest
 
    int f[];      // variable storing the finish time 
                  // of each node in the DFS forest
 
    int t;        // variable storing the current time
 

    DFSInfo(Graph graph) {
       int n = graph.n;
       color = new int[n];
       parent = new int[n];
       d = new int[n];
       f = new int[n];
       t = 0;
    }
    void printDFSInfo(){
      for (int i=1; i<color.length;i++){
         System.out.print(i+": ");
         System.out.print("color:"+color[i]);
         System.out.print(" parent:"+parent[i]);
         System.out.print(" d:"+d[i]);
         System.out.print(" f:"+f[i]+"\n");
      }
    }
 }
 // your "main program" should look something like this:
public class DFSStarter {
    static void recDFS(int u, Graph graph, DFSInfo info) {
       // perform a recursive DFS, starting at u
       info.color[u] = 2;
       info.t += 1;
       info.d[u] = info.t;
       if(graph.A[u]!=null){
          Item node = graph.A[u];
          while(node != null){
             if (info.color[node.data]==1){
                info.parent[node.data] = u;
                recDFS(node.data, graph, info);
            }
             node = node.next;
         }
      }
       info.color[u]=3;
       info.t += 1;
       info.f[u]=info.t;
    }
    static DFSInfo DFS(Graph graph) {
       // performs a "full" DFS on given graph
       DFSInfo info = new DFSInfo(graph);
       for (int i = 1; i<graph.n; i++){
          info.color[i] = 1;
          info.parent[i] = 0;
          info.t = 0;
      }
       for (int j = 1; j<graph.n; j++){
          if (info.color[j]==1){
             recDFS(j, graph, info);
            //System.out.println("One vertex finished.");
         }
      }
      //info.printDFSInfo();
       return info;
      //return null;
    }
    static Item findCycle(Graph graph, DFSInfo info) {
       // If graph contains a cycle x_1 -> ... x_k -> x_1,
       // return a pointer to the head of the linked list
       // (x_1,..., x_k); otherwise, return null.
       // NOTE: if there is a cycle, you should just return
       // one cycle --- it does not matter which one.
 
       // To do this, scan through the edges of graph,
       // using info.f to locate a back edge.
       // Once you find a back edge, use info.parent
       // to build the list of nodes in the cycle
       // in the correct order.
       for (int i=1; i<graph.n;i++){
          Item node = graph.A[i];
          while(node!=null){
             if (info.f[i]<=info.f[node.data]){
                //System.out.println("Find backward Edge!");
                int start = node.data;
                int end = i;
                int parent = info.parent[end];
                Item head = new Item(i, null);
                while (parent!=start){
                  //System.out.print(parent+" ");
                   //cycle.add(parent);
                   head = new Item(parent, head);
                   parent = info.parent[parent];
               }
                head = new Item(node.data, head);
                /*
                System.out.println("Find cycle!");
                System.out.println(i);
                System.out.println(node.data);
                */
                return head;
             }
             node = node.next;
          }
       }
       return null;
    }
    public static void main(String[] args) throws IOException {
       //File text = new File("C:/Users/Petrichor/Desktop/Java/PA4/test6.in");
       FileReader fr=new FileReader("C:/Users/Petrichor/Desktop/Java/PA4/test2.in");
       //InputStreamReader r=new InputStreamReader(System.in);
       //Creating Scanner instnace to read File in Java
       BufferedReader br=new BufferedReader(fr,4096); 
       //BufferedReader reader =  new BufferedReader(new InputStreamReader(System.in));
       //Reading each line of file using Scanner class
       //String line = scnr.nextLine();
       Scanner scnr = new Scanner(br);
       String line = scnr.nextLine();
       String[] command = line.split(" ");
       int edgeNumber = Integer.parseInt(command[1]);
       int verticesNumber = Integer.parseInt(command[0]);
       Graph graph = new Graph(verticesNumber+1);
       //System.out.println("Edge Number: "+edgeNumber);
       //System.out.println("Vertices Number: "+verticesNumber);
       for (int i=0; i<edgeNumber;i++){
          String aline = scnr.nextLine();
          String[] edge = aline.split(" ");
          //System.out.println("u:"+edge[0]+"\tv:"+edge[1]);
          int u = Integer.parseInt(edge[0]);
          int v = Integer.parseInt(edge[1]);
          graph.addEdge(u, v);
      }
       //graph.printGraph();
       //long start2 = System.currentTimeMillis();
       DFSInfo info = DFS(graph);
       //info.printDFSInfo();
       Item cycle = findCycle(graph, info);
       //long finish2 = System.currentTimeMillis();
       //long timeElapsed2 = finish2 - start2;
       //System.out.println("time2: "+timeElapsed2);
       BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out),4096);
       if (cycle == null){
          bw.write("0");
      } 
       else{
          bw.write("1"+"\n");
          while (cycle!=null){
            bw.write(cycle.data+" ");
            cycle = cycle.next;
          }
      }
      bw.flush();
      scnr.close();
    }
 }