using System;

namespace Identity.ViewModels.Token
{
    public interface IToken
    {
        public UInt64 Exp { get; set; }
    }
}