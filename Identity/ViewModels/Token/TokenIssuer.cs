using System;
using System.Text.Json.Serialization;

namespace Identity.ViewModels.Token
{
    public class TokenIssuer : IToken
    {
        [JsonPropertyName("access_token")]
        public AccessToken AccessToken { get; set; }
        [JsonPropertyName("exp")]
        public UInt64 Exp { get; set; }
        [JsonPropertyName("user_id")]
        public string Id { get; set; }
    }
}