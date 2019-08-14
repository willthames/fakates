from __future__ import print_function


def labels_match_selector(labels, selector):
    splits = ['notin', 'in', '!=', '==', '=']
    op = None
    for split in splits:
        if split in selector:
            (left, right) = selector.split(split)
            op = split
            left = left.strip()
            right = right.strip()
            break
    if not op:
        if selector.startswith('!'):
            return selector[1:] not in labels
        else:
            return selector in labels
    if op == '!=':
        return labels[left] != right
    if op == '=' or op == '==':
        return labels[left] == right
    if right.startswith('(') and right.endswith(')'):
        candidates = [item.strip() for item in right[1:-1].split(',')]
        if op == 'notin':
            return labels.get(left) not in candidates
        if op == 'in':
            return labels.get(left) in candidates
    raise RuntimeError


def labels_match_selectors(labels, selectors):
    return all([labels_match_selector(labels, selector)
                for selector in selectors.split(',')])
