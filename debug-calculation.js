// Test calculation to debug the payment amount issue

console.log('=== DEBUGGING PAYMENT CALCULATION ===');

// Values from the contract
const applicableFee = 100000n; // This is what the contract returns (BigInt)
const paymentDuration = 10; // 10 minutes
const tokenDecimals = 8; // HBAR has 8 decimals

// Calculate payment
const durationSeconds = paymentDuration * 60; // 600 seconds
const totalCost = applicableFee * BigInt(durationSeconds);

console.log('applicableFee:', applicableFee.toString());
console.log('durationSeconds:', durationSeconds);
console.log('totalCost (raw):', totalCost.toString());

// Format for display
const divisor = 10n ** BigInt(tokenDecimals);
const formatted = Number(totalCost) / Number(divisor);

console.log('divisor:', divisor.toString());
console.log('formatted amount:', formatted.toFixed(6));

// This should be:
// applicableFee: 100000
// durationSeconds: 600
// totalCost: 60000000
// formatted: 0.600000 HBAR

console.log('Expected: 0.600000 HBAR');
console.log('Matches expectation:', formatted === 0.6);
