const { Kafka, logLevel } = require('kafkajs');


const broker = process.env.kafkaBroker;
const username = process.env.kafkaUsername;
const mechanism = process.env.kafkaSaslMechanism;
const password = process.env.kafkaPassword;
class KafkaProducer {
    constructor() {
        this.kafka = new Kafka({
            brokers: [broker],
            ssl: true,
            sasl: {
                mechanism,
                username,
                password
            },
            connectionTimeout: 5000,
            logLevel: logLevel.ERROR,
        });
        this.producer = this.kafka.producer();
    }

    

    async publish(message) {
        await this.producer.connect();

        await this.producer.send({
            topic: 'user-history',
            messages: [
            { value: message },
            ],
        });

        console.log("Message sent successfully");
        await this.producer.disconnect();
    };
}

module.exports = KafkaProducer;
// const kafkaProducer = new KafkaProducer();

// (async() => {
//     await kafkaProducer.publish('hello');
// })();

// run().catch(e => console.error(e));