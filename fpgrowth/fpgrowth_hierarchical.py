import time
import pandas as pd

from csv import reader
from collections import defaultdict
import numpy as np
from tqdm import tqdm


class Node:
    def __init__(self, itemName, count, parent):
        self.parent = parent
        self.itemName = itemName
        self.count = count
        self.children = {}
        self.next = None

    def increment(self, v):
        self.count += v

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind + 1)


def getFromFile(fname):
    itemSetList = []
    frequency = []

    with open(fname, 'r') as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None, line))
            itemSetList.append(line)
            frequency.append(1)

    return itemSetList, frequency


def constructTree(transactions_list,frequency, minSup):
    sorted_items = defaultdict(int)


    for idx, itemSet in enumerate(transactions_list):

        for item in itemSet:
            sorted_items[item] += frequency[idx]

    # Deleting items below minSup
    sorted_items = dict((item, sup) for item, sup in sorted_items.items() if sup >= minSup)
    if (len(sorted_items) == 0):
        return None, None


    for item in sorted_items:
        sorted_items[item] = [sorted_items[item], None]

    # Init Null head node
    fpTree = Node('Null', 1, None)
    # Update FP tree for each cleaned and sorted itemSet
    for idx, itemSet in tqdm(enumerate(transactions_list)):
        itemSet = [item for item in itemSet if item in sorted_items]
        itemSet.sort(key=lambda item: sorted_items[item][0], reverse=True)
        # Traverse from root to leaf, update tree with given item
        currentNode = fpTree
        for item in itemSet:
            currentNode = updateTree(item, currentNode, sorted_items, frequency[idx])

    return fpTree, sorted_items


def updateSortedTable(item, targetNode, sortedTable):
    if (sortedTable[item][1] == None):
        sortedTable[item][1] = targetNode
    else:
        currentNode = sortedTable[item][1]
        # Traverse to the last node then link it to the target
        while currentNode.next != None:
            currentNode = currentNode.next
        currentNode.next = targetNode


def updateTree(item, treeNode, headerTable, frequency):
    if item in treeNode.children:
        # If the item already exists, increment the count
        treeNode.children[item].increment(frequency)
    else:
        # Create a new branch
        newItemNode = Node(item, frequency, treeNode)
        treeNode.children[item] = newItemNode
        # Link the new branch to header table
        updateSortedTable(item, newItemNode, headerTable)

    return treeNode.children[item]


def ascendFPtree(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.itemName)
        ascendFPtree(node.parent, prefixPath)


def findPrefixPath(item, headerTable):
    # First node in linked list
    treeNode = headerTable[item][1]
    condPats = []
    frequency = []
    while treeNode != None:
        prefixPath = []
        # From leaf node all the way to root
        ascendFPtree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            # Storing the prefix path and it's corresponding count
            condPats.append(prefixPath[1:])
            frequency.append(treeNode.count)

        # Go to next node
        treeNode = treeNode.next
    return condPats, frequency


def traverse_from_childs(headerTable, minSup, _frequentSet, freqItemList):

    sorted_items = sorted(list(headerTable.items()), key=lambda p: p[1][0])
    sortedItemList = [item[0] for item in sorted_items]


    for item in sortedItemList:
        # Pattern growth is achieved by the concatenation of suffix pattern with frequent patterns generated from conditional FP-tree
        newFreqSet = _frequentSet.copy()
        newFreqSet.add(item)
        freqItemList.append(newFreqSet)
        # Find all prefix path, constrcut conditional pattern base
        conditionalPattBase, frequency = findPrefixPath(item, headerTable)
        # Construct conditonal FP Tree with conditional pattern base
        conditionalTree, newHeaderTable = constructTree(conditionalPattBase, frequency, minSup)
        if newHeaderTable != None:
            # Mining recursively on the tree
            traverse_from_childs(newHeaderTable, minSup, newFreqSet, freqItemList)


def powerset(items):
    items_list = list(items)
    n = len(items_list)
    power_set_size = 2 ** n
    all_subsets = []

    for i in range(power_set_size):
        subset = set()
        for j in range(n):
            if (i & (1 << j)) != 0:
                subset.add(items_list[j])
        all_subsets.append(subset)

    return all_subsets

def getSupport(freq_set, transactions_all, transactions_extended, child_parent, dict_levels, childs):
    count = 0

    for idx, t2 in enumerate(transactions_all):
        t2 = set(t2)

        if not freq_set.issubset(t2):
            continue

        parents = []
        for freq_element in freq_set:
            if int(freq_element) in dict_levels[2] or int(freq_element) in dict_levels[1]:
                parents.append(int(freq_element))

        all_parents_supports = True
        for p in parents:
            num_childs_in_transaction = transactions_extended.loc[idx, str(p)]
            num_childs_in_freq_set = len(set(childs[str(p)]) & freq_set)

            if num_childs_in_transaction  <= num_childs_in_freq_set:
                all_parents_supports = False
                break
        if all_parents_supports:
            count += 1

    return count

def set_difference(set1, set2):
    np_set1 = np.array(list(set1))
    np_set2 = np.array(list(set2))
    result = np.setdiff1d(np_set1, np_set2)
    return set(result)
def associationRule(freqItemSet, itemSetList, minConf, rawt, child_parent, dict_levels, childs):
    rules = []
    start_time = time.time_ns()  # Mierzenie czasu rozpoczęcia funkcji
    for itemSet in tqdm(freqItemSet):
        subsets = list(powerset(itemSet))
        itemSetSup = getSupport(itemSet, itemSetList, rawt, child_parent, dict_levels, childs)

        for s in subsets:

            if len(s) == 0 or len(s) == len(itemSet):
                continue

            next_support = getSupport(s, itemSetList, rawt, child_parent, dict_levels, childs)
            if next_support != 0:
                confidence = float(itemSetSup / next_support)
            else:
                confidence = 0.0
            if (confidence > minConf):
                rules.append([set(s), set_difference(itemSet,s), confidence])
    end_time = time.time_ns()  # Mierzenie czasu zakończenia funkcji
    elapsed_time = end_time - start_time  # Obliczanie czasu wykonania funkcji

    return rules

def getFrequency(transactions):
    frequency = np.ones(len(transactions)).tolist()
    return frequency

def remove_single_element_lists(inp):
    result = list()
    for element in inp:
        if not isinstance(element, set) or len(element) > 1:
            result.append(element)
    return result

def map_transaction_list(l, column_map):
    rlist = []
    for t in l:
        newlist = []
        for i in t:
            newlist.append(column_map[i])

        rlist.append(newlist)
    return rlist




def fpgrowth(transactions, minSup, minConf, rawt, child_parent, dict_levels, childs):
    frequency = getFrequency(transactions)

    fpTree, sorted_items = constructTree(transactions,  frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        print('traversing trough tree')
        traverse_from_childs(sorted_items, minSup, set(), freqItems)
        print('discovering rules')
        freq_items_more1 = remove_single_element_lists(freqItems)
        rules = associationRule(freq_items_more1, transactions, minConf, rawt, child_parent, dict_levels, childs)
        return freq_items_more1, rules




def get_levels_dict(dataframe):
    # Utworzenie zbioru zawierającego wszystkie rodzice
    parents = set(dataframe['Ancestors'].str.split(',').sum())

    # Znalezienie elementów, które nie są rodzicami
    leaf_nodes = dataframe[~dataframe['Elements'].isin(parents)]

    # Podział elementów na kategorie na podstawie liczby przodków
    leaf_nodes_dict = {}
    for _, row in leaf_nodes.iterrows():
        ancestors_count = len(row['Ancestors'].split(','))
        if ancestors_count not in leaf_nodes_dict:
            leaf_nodes_dict[ancestors_count] = set()
        set_childs = leaf_nodes_dict[ancestors_count]
        set_childs.add((row['Elements']))

    return leaf_nodes_dict



def get_childs(df):

    taxonomy_dict = {}
    for _, row in df.iterrows():
        parent = str(row[0])
        child = str(row[1])

        if parent not in taxonomy_dict:
            taxonomy_dict[parent] = []

        taxonomy_dict[parent].append(child)
    return taxonomy_dict





def prepare(path):
    taxonomy_dict = pd.read_csv('../dataset/taxonomy_dictionary.csv', header=0)
    dict_levels = get_levels_dict(taxonomy_dict)

    child_parent = pd.read_csv('../dataset/taxonomy.csv', header=0)

    childs = get_childs(child_parent)

    raw_t = pd.read_csv(path, header=0)

    # Example usage:
    transactions_df = pd.read_csv(path, header=0)
    columns = transactions_df.columns
    column_map = {index: column for index, column in enumerate(columns)}

    t_array = transactions_df.values
    transactions_list = [np.nonzero(row)[0].tolist() for row in t_array]
    transactions_list = map_transaction_list(transactions_list, column_map)
    return transactions_list, column_map, raw_t, child_parent, dict_levels, childs

taxonomy_dict = pd.read_csv('../dataset/taxonomy_dictionary.csv', header=0)
leaf_nodes = get_levels_dict(taxonomy_dict)

transaction_list, _, rawt, child_parent, dict_levels, childs = prepare('../dataset/t_200.csv')
freq_itms, rules = fpgrowth(transactions=transaction_list,minSup = 10,minConf = 0.2, rawt=rawt,child_parent=child_parent,  childs = childs, dict_levels = dict_levels )

print("Finded freq items: ", len(freq_itms))
print(freq_itms)
print("Finded rules: ", len(rules))
print(rules)






