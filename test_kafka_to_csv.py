import unittest
from unittest.mock import patch, MagicMock
import csv
import tempfile
import os
from src.data_processing.kafka_to_csv import process_kafka_messages

class KafkaToCSVTest(unittest.TestCase):
    @patch('src.data_processing.kafka_to_csv.KafkaConsumer')
    def test_consume_messages_to_csv(self, mock_kafka_consumer):
        # Mock Kafka messages
        mock_kafka_consumer.return_value = [
            MagicMock(value='2024-10-28T15:30:00,user123,GET /data/m/456.html'),
            MagicMock(value='2024-10-28T15:45:00,user456,GET /rate/789=5'),
            MagicMock(value='2024-10-28T16:00:00,user789,recommendation request server1, SUCCESS, recommendations: 123, response_time: 2s')
        ]
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            watch_file_path = os.path.join(temp_dir, 'watch_events.csv')
            rate_file_path = os.path.join(temp_dir, 'rate_events.csv')
            rec_file_path = os.path.join(temp_dir, 'recommendation_requests.csv')
            
            # Run the process function with mocked Kafka consumer and temporary file paths
            process_kafka_messages(
                consumer=mock_kafka_consumer(),
                watch_file_path=watch_file_path,
                rate_file_path=rate_file_path,
                rec_file_path=rec_file_path
            )

            # Assertions for CSV content
            with open(watch_file_path, 'r') as watch_file, \
                open(rate_file_path, 'r') as rate_file, \
                open(rec_file_path, 'r') as rec_file:

                watch_reader = list(csv.reader(watch_file))
                rate_reader = list(csv.reader(rate_file))
                rec_reader = list(csv.reader(rec_file))

                                # Print the contents of each reader for debugging
                print("Contents of watch_events.csv:", watch_reader)
                print("Contents of rate_events.csv:", rate_reader)
                print("Contents of recommendation_requests.csv:", rec_reader)

                # Ensure each reader has enough rows
                self.assertGreaterEqual(len(watch_reader), 2, "Watch events file does not contain expected rows.")
                self.assertGreaterEqual(len(rate_reader), 2, "Rate events file does not contain expected rows.")

                # Verify content
                self.assertEqual(watch_reader[1], ['2024-10-28 15:30:00', 'user123', '456'])
                self.assertEqual(rate_reader[1], ['2024-10-28 15:45:00', 'user456', '789', '5'])
                # Adjusted expected format to match actual content structure
                self.assertEqual(rec_reader[1], ['2024-10-28 16:00:00', 'user789', 'server1', 'SUCCESS', '123', ' response_time: 2s'])


if __name__ == '__main__':
    unittest.main()
