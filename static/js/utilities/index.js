function convertDecimalToHumanReadable(str, postfix = '₫') {
    const number = parseFloat(str);
    return number.toLocaleString('en-US') + postfix;
}
