//
//  ViewController.swift
//  Perplex
//
//  Created by Marc Lundwall on 16/04/2017.
//  Copyright © 2017 Marc Lundwall. All rights reserved.
//

import Cocoa
import CryptoSwift


// this extension lets us easily select a range/character in a string ("string"[0]=="s" and "string"[2...5]=="ring" are both true)

extension String {
    subscript(pos: Int) -> String {
        precondition(pos >= 0, "character position can't be negative")
        return self[pos...pos]
    }
    subscript(range: Range<Int>) -> String {
        precondition(range.lowerBound >= 0, "range lowerBound can't be negative")
        let lowerIndex = index(startIndex, offsetBy: range.lowerBound, limitedBy: endIndex) ?? endIndex
        return self[lowerIndex..<(index(lowerIndex, offsetBy: range.count, limitedBy: endIndex) ?? endIndex)]
    }
    subscript(range: ClosedRange<Int>) -> String {
        precondition(range.lowerBound >= 0, "range lowerBound can't be negative")
        let lowerIndex = index(startIndex, offsetBy: range.lowerBound, limitedBy: endIndex) ?? endIndex
        return self[lowerIndex..<(index(lowerIndex, offsetBy: range.count, limitedBy: endIndex) ?? endIndex)]
    }
}


// this allows the conversion from hexadecimal to base 64

extension String {
    /// Expanded encoding
    ///
    /// - bytesHexLiteral: Hex string of bytes
    /// - base64: Base64 string
    enum ExpandedEncoding {
        /// Hex string of bytes
        case bytesHexLiteral
        /// Base64 string
        case base64
    }
    
    /// Convert to `Data` with expanded encoding
    ///
    /// - Parameter encoding: Expanded encoding
    /// - Returns: data
    func data(using encoding: ExpandedEncoding) -> Data? {
        switch encoding {
        case .bytesHexLiteral:
            guard self.characters.count % 2 == 0 else { return nil }
            var data = Data()
            var byteLiteral = ""
            for (index, character) in self.characters.enumerated() {
                if index % 2 == 0 {
                    byteLiteral = String(character)
                } else {
                    byteLiteral.append(character)
                    guard let byte = UInt8(byteLiteral, radix: 16) else { return nil }
                    data.append(byte)
                }
            }
            return data
        case .base64:
            return Data(base64Encoded: self)
        }
    }
}


class ViewController: NSViewController {
    
    @IBOutlet weak var FullName: NSTextField!
    @IBOutlet weak var MasterKey: NSSecureTextField!
    @IBOutlet weak var ServiceName: NSTextField!
    @IBOutlet weak var PasswordLabel: NSTextField!



    @IBAction func Button(_ sender: NSButton) {
        
        if(FullName.stringValue != "" || MasterKey.stringValue != "" || ServiceName.stringValue != "")
        {
            PasswordLabel.stringValue = ""
            let pasteBoard = NSPasteboard.general()
            
            pasteBoard.clearContents()
            
        }
        
        if(FullName.stringValue != "" && MasterKey.stringValue != "" && ServiceName.stringValue != "")
        {
        
        
        
        // check to see if a string's sequence contains at least one number, one upper-case letter, and one lower-case letter
        
        func Works(string: String) -> Bool {
            
            let lowerChar = ".*[a-z]+.*"
            let text1 = NSPredicate(format:"SELF MATCHES %@", lowerChar)
            guard text1.evaluate(with: string) else { return false }
            
            let upperChar = ".*[A-Z]+.*"
            let text2 = NSPredicate(format:"SELF MATCHES %@", upperChar)
            guard text2.evaluate(with: string) else { return false }
            
            let digit = ".*[0-9]+.*"
            let text3 = NSPredicate(format:"SELF MATCHES %@", digit)
            guard text3.evaluate(with: string) else { return false }
            
            return true
        }
        
        
        // return the password from the fullname, the masterkey and the website
        
        func Password (fullname: String, masterkey: String, website: String) -> String {
            
            // combine input data into one string
            var ciph = fullname + masterkey + website
            
            // hash input data with SHA-256
            ciph = ciph.sha256()
            print (ciph)
            
            // convert to base 64 and remove unwanted characters ("/" and "+")
            ciph = (ciph.data(using: .bytesHexLiteral)?.base64EncodedString())!
            ciph = ciph.replacingOccurrences(of: "/", with: "")
            ciph = ciph.replacingOccurrences(of: "+", with: "")
            print (ciph)
            print (ciph.characters.count)
            
            // make sure it contains at least one of every character type (A->Z + a->z + 0->9), as well as only different characters
            while Works(string: ciph[0..<12]) == false {
                print (ciph.characters.count)
                // if not, rehash
                ciph = ciph.sha256()
                print (ciph)
                print (ciph.characters.count)
                // convert to base 64 and remove unwanted characters ("/" and "+")
                ciph = (ciph.data(using: .bytesHexLiteral)?.base64EncodedString())!
                ciph = ciph.replacingOccurrences(of: "/", with: "")
                ciph = ciph.replacingOccurrences(of: "+", with: "")
                print (ciph)
            }
            
            // input a "-" every three characters and limit to twelve total characters
            let password = ciph[0..<3] + "-" + ciph[3..<6] + "-" + ciph[6..<9] + "-" + ciph[9..<12]
            
            // return a valid password
            return (password)
            
        }
        
        PasswordLabel.stringValue = Password (fullname: FullName.stringValue , masterkey: MasterKey.stringValue, website: ServiceName.stringValue)
        let pasteBoard = NSPasteboard.general()
        
        pasteBoard.clearContents()
        pasteBoard.writeObjects([PasswordLabel.stringValue as NSPasteboardWriting])
    
    }
        
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.preferredContentSize = NSMakeSize(self.view.frame.size.width, self.view.frame.size.height)
        
        // Do any additional setup after loading the view.
    }

    override var representedObject: Any? {
        didSet {
        // Update the view, if already loaded.
        }
    }


}

