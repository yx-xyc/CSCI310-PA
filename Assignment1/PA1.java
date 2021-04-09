import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;
import java.io.*;

class Node {
   String guide;
   // guide points to max key in subtree rooted at node
}

class InternalNode extends Node {
   Node child0, child1, child2;
   // child0 and child1 are always non-null
   // child2 is null iff node has only 2 children
}

class LeafNode extends Node {
   // guide points to the key

   int value;
}

class TwoThreeTree {
   Node root;
   int height;

   TwoThreeTree() {
      root = null;
      height = -1;
   }
}

class WorkSpace {
// this class is used to hold return values for the recursive doInsert
// routine (see below)

   Node newNode;
   int offset;
   boolean guideChanged;
   Node[] scratch;
}

public class twothree {

   public static void main(String[] args) throws Exception {
       TwoThreeTree database = new TwoThreeTree();
       Scanner scan = new Scanner(System.in);
       BufferedWriter output = new BufferedWriter(new OutputStreamWriter(System.out,"ASCII"), 4096);
       int size = Integer.parseInt(scan.nextLine());
       for (int i =0 ;i<size;i++) {
           String input = scan.nextLine();
           int index = input.indexOf(" ");
           String planet = input.substring(0,index);
           int fee = Integer.parseInt(input.substring(index+1));
           insert(planet, fee, database);
       }
       
       int searchTime = Integer.parseInt(scan.nextLine());
       for (int j = 0; j<searchTime; j++) {
           String input2 = scan.nextLine();
           int index2 = input2.indexOf(" ");
           String small = input2.substring(0,index2);
           String large = input2.substring(index2+1);
           if (small.compareTo(large)>0) {
               large = input2.substring(0,index2);
               small = input2.substring(index2+1);
           }
           
           printRange(small,large,database, output);
       }
    
       output.flush();
       scan.close();
   }

   static void insert(String key, int value, TwoThreeTree tree) {
   // insert a key value pair into tree (overwrite existsing value
   // if key is already present)

      int h = tree.height;

      if (h == -1) {
          LeafNode newLeaf = new LeafNode();
          newLeaf.guide = key;
          newLeaf.value = value;
          tree.root = newLeaf; 
          tree.height = 0;
      }
      else {
         WorkSpace ws = doInsert(key, value, tree.root, h);

         if (ws != null && ws.newNode != null) {
         // create a new root

            InternalNode newRoot = new InternalNode();
            if (ws.offset == 0) {
               newRoot.child0 = ws.newNode; 
               newRoot.child1 = tree.root;
            }
            else {
               newRoot.child0 = tree.root; 
               newRoot.child1 = ws.newNode;
            }
            resetGuide(newRoot);
            tree.root = newRoot;
            tree.height = h+1;
         }
      }
   }

   static WorkSpace doInsert(String key, int value, Node p, int h) {
   // auxiliary recursive routine for insert

      if (h == 0) {
         // we're at the leaf level, so compare and 
         // either update value or insert new leaf

         LeafNode leaf = (LeafNode) p; //downcast
         int cmp = key.compareTo(leaf.guide);

         if (cmp == 0) {
            leaf.value = value; 
            return null;
         }

         // create new leaf node and insert into tree
         LeafNode newLeaf = new LeafNode();
         newLeaf.guide = key; 
         newLeaf.value = value;

         int offset = (cmp < 0) ? 0 : 1;
         // offset == 0 => newLeaf inserted as left sibling
         // offset == 1 => newLeaf inserted as right sibling

         WorkSpace ws = new WorkSpace();
         ws.newNode = newLeaf;
         ws.offset = offset;
         ws.scratch = new Node[4];

         return ws;
      }
      else {
         InternalNode q = (InternalNode) p; // downcast
         int pos;
         WorkSpace ws;

         if (key.compareTo(q.child0.guide) <= 0) {
            pos = 0; 
            ws = doInsert(key, value, q.child0, h-1);
         }
         else if (key.compareTo(q.child1.guide) <= 0 || q.child2 == null) {
            pos = 1;
            ws = doInsert(key, value, q.child1, h-1);
         }
         else {
            pos = 2; 
            ws = doInsert(key, value, q.child2, h-1);
         }

         if (ws != null) {
            if (ws.newNode != null) {
               // make ws.newNode child # pos + ws.offset of q

               int sz = copyOutChildren(q, ws.scratch);
               insertNode(ws.scratch, ws.newNode, sz, pos + ws.offset);
               if (sz == 2) {
                  ws.newNode = null;
                  ws.guideChanged = resetChildren(q, ws.scratch, 0, 3);
               }
               else {
                  ws.newNode = new InternalNode();
                  ws.offset = 1;
                  resetChildren(q, ws.scratch, 0, 2);
                  resetChildren((InternalNode) ws.newNode, ws.scratch, 2, 2);
               }
            }
            else if (ws.guideChanged) {
               ws.guideChanged = resetGuide(q);
            }
         }

         return ws;
      }
   }


   static int copyOutChildren(InternalNode q, Node[] x) {
   // copy children of q into x, and return # of children

      int sz = 2;
      x[0] = q.child0; x[1] = q.child1;
      if (q.child2 != null) {
         x[2] = q.child2; 
         sz = 3;
      }
      return sz;
   }

   static void insertNode(Node[] x, Node p, int sz, int pos) {
   // insert p in x[0..sz) at position pos,
   // moving existing extries to the right

      for (int i = sz; i > pos; i--)
         x[i] = x[i-1];

      x[pos] = p;
   }

   static boolean resetGuide(InternalNode q) {
   // reset q.guide, and return true if it changes.

      String oldGuide = q.guide;
      if (q.child2 != null)
         q.guide = q.child2.guide;
      else
         q.guide = q.child1.guide;

      return q.guide != oldGuide;
   }


   static boolean resetChildren(InternalNode q, Node[] x, int pos, int sz) {
   // reset q's children to x[pos..pos+sz), where sz is 2 or 3.
   // also resets guide, and returns the result of that

      q.child0 = x[pos]; 
      q.child1 = x[pos+1];

      if (sz == 3) 
         q.child2 = x[pos+2];
      else
         q.child2 = null;

      return resetGuide(q);
   }
   
   static void printRange(String x, String y, TwoThreeTree tree, BufferedWriter output) throws Exception {
       if (tree.height==-1) {
           return;
       }
       
       Node[] searchPath1 = search(x,tree);
       Node[] searchPath2 = search(y,tree);
       
       int divergePos = 0;
       while (divergePos<tree.height+1&&searchPath1[divergePos]==searchPath2[divergePos]) {
           divergePos++;
       }
       divergePos--;
       
       if (divergePos==tree.height) {
           LeafNode leaf = (LeafNode) searchPath1[divergePos];
           if (leaf.guide.compareTo(x)>=0&&leaf.guide.compareTo(y)<=0) {
               String print = leaf.guide + " " + leaf.value + "\n";
               output.write(print);
           }
           return;
       }
       
       InternalNode div = (InternalNode) searchPath1[divergePos];
       LeafNode leaf1 = (LeafNode) searchPath1[tree.height];
       LeafNode leaf2 = (LeafNode) searchPath2[tree.height];
       
       if (leaf1.guide.compareTo(x)>=0) {
           String print = leaf1.guide + " " + leaf1.value + "\n";
           output.write(print);
       }
       
       for (int m = tree.height-1; m>divergePos; m--) {
           Node lastNode = searchPath1[m+1];
           InternalNode cur = (InternalNode) searchPath1[m];
           if (cur.child1.guide.compareTo(lastNode.guide)>0) {
              printAll(cur.child1, tree.height-m-1, output);
           }
           if (cur.child2!=null&&cur.child2.guide.compareTo(lastNode.guide)>0) {
              printAll(cur.child2, tree.height-m-1, output);
           }
       }
       
       if (div.child0==searchPath1[divergePos+1]&&div.child2==searchPath2[divergePos+1]) {
           printAll(div.child1,tree.height-divergePos-1, output);
       }
       
       for (int m = divergePos+1; m<tree.height; m++) {
           Node nextNode = searchPath2[m+1];
           InternalNode cur = (InternalNode) searchPath2[m];
           if (cur.child0.guide.compareTo(nextNode.guide)<0) {
              printAll(cur.child0, tree.height-m-1, output);
           }
           if (cur.child1!=null&&cur.child1.guide.compareTo(nextNode.guide)<0) {
              printAll(cur.child1, tree.height-m-1, output);
           }
       }
       
       if (leaf2.guide.compareTo(y)<=0) {
           String print = leaf2.guide + " " + leaf2.value + "\n";
           output.write(print);
       }
       
   }
   
   static void printAll (Node p, int h, BufferedWriter output) throws Exception {
       if (p==null) {
           return;
       }
       if (h==0) {
           LeafNode w = (LeafNode) p;
           String print = w.guide + " " + w.value + "\n";
           output.write(print);
       } else {
           InternalNode w = (InternalNode) p;
          printAll(w.child0,h-1, output);
          printAll(w.child1,h-1, output);
          printAll(w.child2,h-1, output);
       }
   }
   
   static Node[] search (String key, TwoThreeTree tree) {
       Node[] path_Recorder = new Node[tree.height+1];
       
       if (tree.height==0) {
               path_Recorder[0] = tree.root;
       } else {
           InternalNode cur = (InternalNode)tree.root;
           path_Recorder[0] = tree.root;
           for (int i=1; i<tree.height;i++) {
               if (key.compareTo(cur.child0.guide)<=0) {
                   path_Recorder[i] = cur.child0;
                   cur = (InternalNode) cur.child0;
               } else if (cur.child2==null||key.compareTo(cur.child1.guide)<=0) {
                   path_Recorder[i] = cur.child1;
                   cur = (InternalNode) cur.child1;
               } else {
                   path_Recorder[i] = cur.child2;
                   cur = (InternalNode) cur.child2;
               }
           }
           
           if (key.compareTo(cur.child0.guide)<=0) {
               path_Recorder[tree.height] = cur.child0;
           } else if (cur.child2==null||key.compareTo(cur.child1.guide)<=0) {
               path_Recorder[tree.height] = cur.child1;
           } else {
               path_Recorder[tree.height] = cur.child2;
           }
           
       }
       
       return path_Recorder;
   }
   
}


