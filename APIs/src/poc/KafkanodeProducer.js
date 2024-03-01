const kafka = require('kafka-node');

const client = new kafka.KafkaClient({
  kafkaHost: 'dory.srvs.cloudkafka.com:9094', // Replace with your broker address
  sslOptions: {
    rejectUnauthorized: false, // Disable SSL certificate verification (for development purposes)
  },
  sasl: {
    mechanism: 'SCRAM-SHA-512',
    username: process.env.username, // Store username securely
    password: process.env.password, // Store password securely
},
});

const producer = new kafka.Producer(client);

// Connect to the Kafka broker
producer.on('ready', function () {
  console.log('Producer is ready');

  // Produce a message to a Kafka topic
  const topicName = 'cdzbgqqu-test';
  const payloads = [
    {
      topic: topicName,
      messages: 'Hello, Kafka!',
    },
  ];

  producer.send(payloads, function (err, data) {
    if (err) {
      console.error('Error producing message: ', err);
    } else {
      console.log('Message produced successfully: ', data);
    }
  });
});

// Handle producer errors
producer.on('error', function (err) {
  console.error('Error in Kafka producer: ', err);
});

// Gracefully shut down the producer on process termination
process.on('SIGINT', function () {
  producer.close(function () {
    console.log('Producer closed');
    process.exit();
  });
});
