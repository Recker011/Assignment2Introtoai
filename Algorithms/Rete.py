from Parse import Parse

class Node:
    def __init__(self, pattern):
        self.pattern = pattern
        self.children = []
        self.memory = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_fact(self, fact):
        self.memory.append(fact)

class Rete:
    @staticmethod
    def implies(fact):
        # Returns the right side of the implication if it exists
        return fact.split('=>')[1] if '=>' in fact else None

    @staticmethod
    def entails(fact):
        # Returns a sorted list of premises if it exists
        return sorted(fact.split('=>')[0].split('&')) if '=>' in fact else []

    @staticmethod
    def is_fact(fact):
        # Returns True if the fact is not an implication
        return '=>' not in fact

    @staticmethod
    def check(KB, query):
        #kbtype = Parse.checkkbtype(KB)
        kbtype = "HC"
        if kbtype == "HC":
            # Initialize network with facts from KB
            root = Node(None)
            for fact in KB:
                premises = Rete.entails(fact)
                current_node = root
                for premise in premises:
                    # Find child node with given pattern and no memory
                    child_node = next((child for child in current_node.children if child.pattern == premise and not child.memory), None)
                    if not child_node:
                        child_node = Node(premise)
                        current_node.add_child(child_node)
                    current_node = child_node
                #leaf_node = Node(Rete.implies(fact).strip())
                implies_fact = Rete.implies(fact)
                if implies_fact:
                    leaf_node = Node(Rete.implies(fact).strip())
                else:
                    leaf_node = Node(None)
                    
                current_node.add_child(leaf_node)

            # Initialize agenda with facts from KB
            agenda = [fact for fact in KB if Rete.is_fact(fact)]

            # Add right side of implication to agenda if it exists
            for fact in KB:
                if Rete.implies(fact):
                    agenda.append(Rete.implies(fact))

            entailed_facts = []

            while agenda:
                p = agenda.pop(0)

                # If p matches the query, return YES with entailed facts
                if p == query[0]:
                    entailed_facts.append(p)
                    return f'YES: {", ".join(entailed_facts)}'

                # Add p to memory of all leaf nodes with pattern p
                stack = [root]
                while stack:
                    node = stack.pop()
                    if not node.children and node.pattern == p:
                        node.add_fact(p)
                    stack.extend(node.children)

                # Check if any leaf nodes have all premises satisfied
                stack = [root]
                while stack:
                    node = stack.pop()
                    if not node.children:
                        # Leaf node reached
                        current_node = node.parent
                        while current_node != root:
                            # Check if all children have memory
                            if not all(child.memory for child in current_node.children if child.pattern):
                                break
                            current_node = current_node.parent
                        else:
                            q = node.pattern
                            if q and q not in entailed_facts:
                                agenda.append(q)  # Add new facts to front of agenda

                                # Add new facts to entailed_facts list after checking if they match query
                                if q == query[0]:
                                    entailed_facts.append(q)

            return 'NO'
        else:
            return "The Knowledge Base is not in Horn Clause format"