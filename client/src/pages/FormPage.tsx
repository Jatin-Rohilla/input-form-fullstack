import { useState } from 'react';
import { useForm } from 'react-hook-form';
import {
    Box, Button, Container, FormControl, FormLabel, Input, Textarea,
    FormErrorMessage, Heading, VStack, useToast, HStack
} from '@chakra-ui/react';
import { submitForm } from '../services/api';
import { FormData } from '../types';
import ReactSelect from 'react-select';

// Define type for country code option
type CountryCodeOption = {
    value: string;
    label: string;
};

const countryCodes: CountryCodeOption[] = [
    { value: '+1', label: 'USA/Canada (+1)' },
    { value: '+44', label: 'UK (+44)' },
    { value: '+91', label: 'India (+91)' },
    { value: '+61', label: 'Australia (+61)' },
    { value: '+49', label: 'Germany (+49)' },
    { value: '+33', label: 'France (+33)' },
    { value: '+86', label: 'China (+86)' },
    { value: '+81', label: 'Japan (+81)' },
];

const FormPage = () => {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [selectedCountryCode, setSelectedCountryCode] = useState<CountryCodeOption>(countryCodes[0]);
    const toast = useToast();

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors }
    } = useForm<Omit<FormData, 'id' | 'createdAt' | 'countryCode'>>();

    const onSubmit = async (data: Omit<FormData, 'id' | 'createdAt' | 'countryCode'>) => {
        try {
            setIsSubmitting(true);
            const formData: Omit<FormData, 'id' | 'createdAt'> = {
                ...data,
                countryCode: selectedCountryCode.value
            };

            await submitForm(formData);

            toast({
                title: 'Success!',
                description: 'Your message has been submitted.',
                status: 'success',
                duration: 5000,
                isClosable: true,
            });

            reset();
            setSelectedCountryCode(countryCodes[0]);
        } catch (error) {
            toast({
                title: 'Error',
                description: 'There was an error submitting your message.',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
            console.error(error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Container maxW="container.md" py={10}>
            <VStack spacing={8} align="stretch">
                <Heading as="h1" textAlign="center">Contact Form</Heading>

                <Box as="form" onSubmit={handleSubmit(onSubmit)} p={6} borderWidth={1} borderRadius="lg" shadow="md">
                    <VStack spacing={4} align="stretch">
                        <FormControl isInvalid={!!errors.name} isRequired>
                            <FormLabel>Name</FormLabel>
                            <Input
                                {...register('name', {
                                    required: 'Name is required',
                                    minLength: { value: 2, message: 'Name must be at least 2 characters' }
                                })}
                            />
                            <FormErrorMessage>{errors.name?.message}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.email} isRequired>
                            <FormLabel>Email</FormLabel>
                            <Input
                                type="email"
                                {...register('email', {
                                    required: 'Email is required',
                                    pattern: {
                                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                        message: 'Invalid email address'
                                    }
                                })}
                            />
                            <FormErrorMessage>{errors.email?.message}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.phoneNumber} isRequired>
                            <FormLabel>Phone Number</FormLabel>
                            <HStack>
                                <Box width="40%">
                                    <ReactSelect
                                        options={countryCodes}
                                        value={selectedCountryCode}
                                        onChange={(option) => setSelectedCountryCode(option as CountryCodeOption)}
                                        isSearchable
                                    />
                                </Box>
                                <Input
                                    flex={1}
                                    {...register('phoneNumber', {
                                        required: 'Phone number is required',
                                        pattern: {
                                            value: /^[0-9]{7,15}$/,
                                            message: 'Please enter a valid phone number'
                                        }
                                    })}
                                    placeholder="Phone number"
                                />
                            </HStack>
                            <FormErrorMessage>{errors.phoneNumber?.message}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.message} isRequired>
                            <FormLabel>Message</FormLabel>
                            <Textarea
                                {...register('message', {
                                    required: 'Message is required',
                                    minLength: { value: 10, message: 'Message must be at least 10 characters' }
                                })}
                                rows={5}
                            />
                            <FormErrorMessage>{errors.message?.message}</FormErrorMessage>
                        </FormControl>

                        <Button
                            type="submit"
                            colorScheme="blue"
                            width="full"
                            mt={4}
                            isLoading={isSubmitting}
                        >
                            Submit
                        </Button>
                    </VStack>
                </Box>
            </VStack>
        </Container>
    );
};

export default FormPage; 