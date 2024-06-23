const sequenceSum = (begin, end, step) => {
  // May the Force be with you
  if (begin > end) {
    return 0;
  }
  let sum = 0;
  let sequence = begin;
  while (sequence <= end) {
    sum += sequence;
    sequence += step;
  }
  return sum;
};

// console.log(sequenceSum(2, 6, 2));
