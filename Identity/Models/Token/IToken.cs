using System;

namespace Identity.Models.Token
{
    public interface IToken
    {
        public string Aud { get; set; }
        public string Iss { get; set; }
        public string Sub { get; set; }
        public string Jti { get; set; }
        public UInt64 Exp { get; set; }
    }
}