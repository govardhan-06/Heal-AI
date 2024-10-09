// ignore_for_file: prefer_const_constructors

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:healai/pages/dochomepage.dart';
import 'package:healai/services/docloginorreg.dart';

class DocAuthGate extends StatelessWidget {
  const DocAuthGate({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: StreamBuilder(
        stream: FirebaseAuth.instance.authStateChanges(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return DocHomePage();
          } else {
            return const DocLoginOrReg();
          }
        },
      ),
    );
  }
}
