import SwiftUI

struct SalangCoffeeProfilePage: View {
    var body: some View {
        NavigationView {
            VStack {
                Image("salang_coffee_logo") // Placeholder for the logo
                    .resizable()
                    .scaledToFit()
                    .frame(width: 100, height: 100)
                    .clipShape(Circle())
                    .padding()

                Text("Welcome to Salang Coffee!")
                    .font(.title)
                    .fontWeight(.bold)
                    .padding()

                Text("Your favorite place for premium coffee.")
                    .font(.subheadline)
                    .foregroundColor(.gray)
                    .padding()

                List {
                    Section(header: Text("Profile Information")) {
                        Text("Name: John Doe") // Placeholder
                        Text("Email: johndoe@example.com") // Placeholder
                    }

                    Section(header: Text("Settings")) {
                        NavigationLink(destination: Text("Order History")) {
                            Text("Order History")
                        }
                        NavigationLink(destination: Text("Account Settings")) {
                            Text("Account Settings")
                        }
                    }
                }
            }
            .navigationTitle("Profile")
        }
    }
}

struct SalangCoffeeProfilePage_Previews: PreviewProvider {
    static var previews: some View {
        SalangCoffeeProfilePage()
    }
}