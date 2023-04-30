from dataclasses import dataclass, field
from typing import List, Optional
import libcst as cst
import tiktoken
from write_the.cst.docstring_remover import remove_docstrings
from write_the.cst.node_extractor import extract_node_from_tree, extract_nodes_from_tree
from write_the.cst.node_remover import remove_nodes_from_tree
from write_the.cst.utils import get_code_from_node, nodes_to_tree
from write_the.cst.function_and_class_collector import get_node_names


class Node:
    """
    A class representing a node in a CST tree.
    Args:
      name (str): The name of the node.
      node (cst.CSTNode): The CST node.
      code (str): The code of the node.
      tokens (int): The number of tokens in the node.
    """

    name: str
    node: cst.CSTNode
    code: str
    tokens: int

    def __init__(self, *, tree, node_name, response_size=80) -> None:
        """
        Initializes a Node object.
        Args:
          tree (cst.Module): The CST tree.
          node_name (str): The name of the node.
          response_size (int): The size of the response.
        """
        self.node = extract_node_from_tree(tree=tree, node=node_name)
        self.name = node_name
        self.code = get_code_from_node(self.node)
        encoding = tiktoken.encoding_for_model("gpt-4")
        self.tokens = len(encoding.encode(self.code)) + response_size


class Background(Node):
    """
    A class representing a background in a CST tree.
    Args:
      body (cst.CSTNode): The CST node of the background.
    """

    def __init__(self, body) -> None:
        """
        Initializes a Background object.
        Args:
          body (cst.CSTNode): The CST node of the background.
        """
        self.node = body
        self.name = "background"
        self.code = self.node.code
        encoding = tiktoken.encoding_for_model("gpt-4")
        self.tokens = len(encoding.encode(self.code))


@dataclass
class NodeBatch:
    """
    A class representing a batch of nodes in a CST tree.
    Args:
      tree (cst.Module): The CST tree.
      background (Optional[Background]): The background of the tree.
      max_tokens (int): The maximum number of tokens in the batch.
      prompt_size (int): The size of the prompt.
      nodes (List[Node]): The list of nodes in the batch.
      max_batch_size (Optional[int]): The maximum size of the batch.
      send_node_context (bool): Whether to send the context of the nodes.
    """

    tree: cst.Module
    background: Optional[Background]
    max_tokens: int
    prompt_size: int
    nodes: List[Node] = field(default_factory=list)
    max_batch_size: Optional[int] = None
    send_node_context: bool = False

    @property
    def tokens(self) -> int:
        """
        Gets the number of tokens in the batch.
        Returns:
          int: The number of tokens in the batch.
        """
        tokens = self.prompt_size + sum(n.tokens for n in self.nodes)
        if self.background:
            tokens += self.background.tokens
        return tokens

    @property
    def node_names(self) -> List[str]:
        """
        Gets the names of the nodes in the batch.
        Returns:
          List[str]: The names of the nodes in the batch.
        """
        return [n.name for n in self.nodes]

    @property
    def space_available(self) -> int:
        """
        Gets the amount of space available in the batch.
        Returns:
          int: The amount of space available in the batch.
        """
        return self.max_tokens - self.tokens

    @property
    def code(self):
        """
        Gets the code of the batch.
        Returns:
          str: The code of the batch.
        """
        if self.send_node_context:
            # send everything
            return self.tree.code
        if self.background:
            # remove all non batch nodes
            all_nodes = get_node_names(self.tree, True)
            classes_to_keep = [n.split(".")[0] for n in self.node_names if "." in n]
            nodes_to_remove: List[str] = [
                n for n in all_nodes if n not in self.node_names
            ]
            nodes_to_remove = [n for n in nodes_to_remove if n not in classes_to_keep]
            processed_tree = remove_nodes_from_tree(self.tree, nodes_to_remove)
        else:
            # extract batch nodes
            extracted_nodes = extract_nodes_from_tree(self.tree, self.node_names)
            processed_tree = nodes_to_tree(extracted_nodes)
        return processed_tree.code

    def add(self, node: Node):
        """
        Adds a node to the batch.
        Args:
          node (Node): The node to add.
        Raises:
          ValueError: If there is no space available in the batch.
        """
        if self.space_available - node.tokens < 0 or (
            self.max_batch_size and len(self.nodes) + 1 > self.max_batch_size
        ):
            raise ValueError("No space available in batch!")
        self.nodes.append(node)


def extract_background(tree):
    """
    Extracts the background from a CST tree.
    Args:
      tree (cst.Module): The CST tree.
    Returns:
      Background: The background of the tree.
    """
    all_node_names = get_node_names(tree, force=True)
    background = remove_nodes_from_tree(tree, all_node_names)
    return Background(body=background)


def create_batches(
    tree,
    node_names,
    max_tokens,
    prompt_size,
    response_size_per_node,
    max_batch_size=None,
    send_background_context=True,
    send_node_context=True,
) -> List[NodeBatch]:
    """
    Creates batches of nodes from a tree.
    Args:
      tree (cst.Module): The tree to create batches from.
      node_names (List[str]): The names of the nodes to create batches for.
      max_tokens (int): The maximum number of tokens per batch.
      prompt_size (int): The size of the prompt for each node.
      response_size_per_node (int): The size of the response for each node.
      max_batch_size (Optional[int]): The maximum number of nodes per batch.
      send_background_context (bool): Whether to send background context.
      send_node_context (bool): Whether to send node context.
    Returns:
      List[NodeBatch]: A list of batches of nodes.
    Examples:
      >>> create_batches(tree, node_names, max_tokens, prompt_size, response_size_per_node)
      [NodeBatch(...), NodeBatch(...)]
    """
    tree = remove_docstrings(tree, node_names)  # TODO: fix to use Class.method syntax
    batches = []
    background = None
    if send_background_context:
        background = extract_background(tree)

    def create_batch():
        """
        Creates a batch of nodes from a tree.
        Args:
          tree (cst.Module): The tree to create batches from.
          max_tokens (int): The maximum number of tokens per batch.
          prompt_size (int): The size of the prompt for each node.
          background (Optional[cst.Module]): The background context for the batch.
          max_batch_size (Optional[int]): The maximum number of nodes per batch.
          send_node_context (bool): Whether to send node context.
        Returns:
          NodeBatch: A batch of nodes.
        Examples:
          >>> create_batch(tree, max_tokens, prompt_size, background, max_batch_size, send_node_context)
          NodeBatch(...)
        """
        return NodeBatch(
            tree=tree,
            max_tokens=max_tokens,
            prompt_size=prompt_size,
            background=background,
            max_batch_size=max_batch_size,
            send_node_context=send_node_context,
        )

    current_batch = create_batch()
    for node_name in node_names:
        node = Node(
            tree=tree, node_name=node_name, response_size=response_size_per_node
        )
        try:
            current_batch.add(node)
        except ValueError:
            # full
            batches.append(current_batch)
            current_batch = create_batch()
            current_batch.add(node)
    batches.append(current_batch)
    return batches
