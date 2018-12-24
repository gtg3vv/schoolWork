public Class Node {
    private int num;
    private String value;
    private Node previous;
    private Node next;
    
    public Node(int num, String value)
    {
        this.num = num;
        this.value = value;
        this.previous = null;
        this.next = null;
    }
    
    public Node()
    {
        this.num = null;
        this.value = null;
        this.previous = null;
        this.next = null;
    }
    
    public void setPrevious(Node n){
        this.previous = n;
    }
    public Node getPrevious()
    {
        return this.previous;
    }
    public void setNext(Node n)
    {
        this.next = m;
    }
    public Node getNext(){
        return this.next;
    }
}