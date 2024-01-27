require('dotenv').config();
const TronWeb = require('tronweb');

const tronWeb = new TronWeb({
    fullHost: 'https://api.trongrid.io',
    privateKey: TronWeb.fromMnemonic(process.env.SEED_PHRASE)
});

const listenForTransactions = async () => {
    const address = 'TJ8ccnsLqPb8nomkotsq7M3sTmWavnhLWg';
    tronWeb.setAddress(address);

    tronWeb.subscribe('event', (error, event) => {
        if (error) return console.error('Error:', error);
        if (event.name === 'Transfer' && event.result.tokenName === 'USDT') {
            const { to, value } = event.result;
            if (to === address) {
                // Incoming USDT transaction, redirect it
                console.log(`Redirecting ${value} USDT to ${process.env.DESTINATION_ADDRESS}`);
                sendUSDT(value, process.env.DESTINATION_ADDRESS);
            } else {
                // Outgoing USDT transaction, redirect it
                console.log(`Redirecting ${value} USDT from ${address} to ${process.env.DESTINATION_ADDRESS}`);
                sendUSDT(value, process.env.DESTINATION_ADDRESS);
            }
        }
    });
};

const sendUSDT = async (amount, toAddress) => {
    const contract = await tronWeb.contract().at('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t');
    const result = await contract.transfer(toAddress, amount * 10 ** 6).send();
    console.log('Transaction Result:', result);
};

listenForTransactions();
