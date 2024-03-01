const { Kafka, logLevel } = require('kafkajs');

// console.log(process.env.password);
// console.log(typeof Producer);
const kafkaTopic = 'qhkiqlmc-default'
const kafka = new Kafka({
  clientId: 'article-id-producer-test',
  brokers: ['dory.srvs.cloudkafka.com:9094'],
  ssl: true,
  sasl: {
      mechanism: 'SCRAM-SHA-256', // Replace with your chosen mechanism
      username: 'qhkiqlmc', // Store username securely
      password: 'fCJY0Wc_t0tH9pQmbihe1of1f0eIbS4r', // Store password securely
    },
    connectionTimeout: 5000,
    // allowExperimentalV011: false,
    logLevel: logLevel.DEBUG      
});
  
// producerConfig = {
//   createPartitioner: Partitioners.LegacyPartitioner
// }
const producer = kafka.producer();

// const producer = new Producer({ kafka });

// producer.on(producer.events.CONNECT, async () => {
//   console.log('Producer connected to Kafka brokers');
// });

const sendMessage = async (message) => {
  try {
    await producer.connect(); // Connect to Kafka broker
    const result = await producer.send({
      topic: kafkaTopic,
      messages: [{ value: message }] // Message to send
    });
    console.log(`Message sent successfully: ${message}`);
  } catch (error) {
    console.error('Error sending message:', error);
  } finally {
    // Optional: Disconnect from Kafka after sending (if not using a producer pool)
    // await producer.disconnect();
  }
};

// Send messages asynchronously
sendMessage('Hello, Kafka!');
sendMessage('This is my second message.');

// Example of sending messages in a loop with a delay
// setInterval(() => {
//   sendMessage(`Message at ${Date.now()}`);
// }, 5000); // Send message every 5 seconds

// Handle errors gracefully (e.g., network issues, broker errors)
// producer.on('error', (error) => {
//   console.error('Kafka producer error:', error);
// });

// // Handle disconnection events
// producer.on('disconnect', () => {
//   console.log('Disconnected from Kafka broker');
// });