//criar um form para receber prova e aluno

import React, { Component } from 'react';
import { View, Text, StyleSheet, TextInput, Button, Alert } from 'react-native';

export default class Form extends Component {
    
        constructor(props) {
            super(props);
            this.state = {
                prova: '',
                aluno: ''
            };
        }
    
        render() {
            return (
                <View style={styles.container}>
                    <Text style={styles.text}>Prova:</Text>
                    <TextInput
                        style={styles.input}
                        onChangeText={(prova) => this.setState({ prova })}
                        value={this.state.prova}
                    />
                    <Text style={styles.text}>Aluno:</Text>
                    <TextInput
                        style={styles.input}
                        onChangeText={(aluno) => this.setState({ aluno })}
                        value={this.state.aluno}
                    />
                    <Button
                        title="Salvar"
                        onPress={() => {
                            Alert.alert('Prova: ' + this.state.prova + ' Aluno: ' + this.state.aluno);
                        }}
                    />
                </View>
            );
        }
    }

    const styles = StyleSheet.create({
        container: {
            flex: 1,
            padding: 10,
            backgroundColor: '#fff'
        },
        text: {
            fontSize: 20,
            fontWeight: 'bold'
        },
        input: {
            height: 40,
            borderColor: 'gray',
            borderWidth: 1,
            marginBottom: 10
        }
    });

// Path: index.js