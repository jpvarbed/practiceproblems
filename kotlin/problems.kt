fun arrayTransformation(array: Array<Int>): Array<Int> {
    val min = array.minOrNull();
    if (min == null) return array;
    array.map({ abs(it - min)  }).toTypedArray();
}