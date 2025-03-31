import { useEffect, useState } from 'react';
import {
    Box, Container, Heading, Table, Thead, Tbody, Tr, Th, Td,
    TableContainer, Text, Spinner, Button, HStack, useToast
} from '@chakra-ui/react';
import { getAllSubmissions } from '../services/api';
import { FormData } from '../types';
import { Link } from 'react-router-dom';

const SubmissionsPage = () => {
    const [submissions, setSubmissions] = useState<FormData[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const toast = useToast();

    const fetchSubmissions = async () => {
        try {
            setIsLoading(true);
            setError('');
            const data = await getAllSubmissions();
            setSubmissions(data);
        } catch (error) {
            console.error('Error fetching submissions:', error);
            setError('Failed to load submissions. Please try again later.');
            toast({
                title: 'Error',
                description: 'Failed to load submissions.',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchSubmissions();
    }, []);

    return (
        <Container maxW="container.xl" py={10}>
            <HStack mb={6} justifyContent="space-between">
                <Heading as="h1">Form Submissions</Heading>
                <Button as={Link} to="/" colorScheme="blue">
                    Back to Form
                </Button>
            </HStack>

            {isLoading ? (
                <Box textAlign="center" py={10}>
                    <Spinner size="xl" />
                    <Text mt={4}>Loading submissions...</Text>
                </Box>
            ) : error ? (
                <Box textAlign="center" py={10}>
                    <Text color="red.500">{error}</Text>
                    <Button mt={4} onClick={fetchSubmissions} colorScheme="blue">
                        Try Again
                    </Button>
                </Box>
            ) : submissions.length === 0 ? (
                <Box textAlign="center" py={10} borderWidth={1} borderRadius="lg" borderColor="gray.200">
                    <Text fontSize="lg">No submissions found.</Text>
                    <Button as={Link} to="/" mt={4} colorScheme="blue">
                        Create new submission
                    </Button>
                </Box>
            ) : (
                <TableContainer borderWidth={1} borderRadius="lg" shadow="md">
                    <Table variant="simple">
                        <Thead bg="gray.100">
                            <Tr>
                                <Th>Name</Th>
                                <Th>Email</Th>
                                <Th>Phone</Th>
                                <Th>Message</Th>
                                <Th>Submitted At</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {submissions.map((submission) => (
                                <Tr key={submission.id}>
                                    <Td>{submission.name}</Td>
                                    <Td>{submission.email}</Td>
                                    <Td>{`${submission.country_code} ${submission.phone_number}`}</Td>
                                    <Td maxW="300px" isTruncated title={submission.message}>
                                        {submission.message}
                                    </Td>
                                    <Td>
                                        {submission.createdAt
                                            ? new Date(submission.createdAt).toLocaleString()
                                            : 'N/A'}
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    </Table>
                </TableContainer>
            )}
        </Container>
    );
};

export default SubmissionsPage; 