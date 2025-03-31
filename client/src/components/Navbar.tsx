import { Box, Flex, Heading, Button, HStack } from '@chakra-ui/react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    return (
        <Box as="nav" bg="blue.600" color="white" py={3} px={5} shadow="md">
            <Flex justify="space-between" align="center">
                <Heading size="md">Form App</Heading>
                <HStack spacing={4}>
                    <Button
                        as={Link}
                        to="/"
                        colorScheme="blue"
                        variant={location.pathname === '/' ? 'solid' : 'ghost'}
                        size="sm"
                    >
                        Form
                    </Button>
                    <Button
                        as={Link}
                        to="/submissions"
                        colorScheme="blue"
                        variant={location.pathname === '/submissions' ? 'solid' : 'ghost'}
                        size="sm"
                    >
                        Submissions
                    </Button>
                </HStack>
            </Flex>
        </Box>
    );
};

export default Navbar; 