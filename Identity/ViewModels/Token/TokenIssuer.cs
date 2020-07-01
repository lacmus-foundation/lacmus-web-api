using System;
using System.Text.Json.Serialization;
using Identity.Models.Token;

namespace Identity.ViewModels.Token
{
    public class TokenIssuer
    {
        [JsonPropertyName("access_token")]
        public AccessToken AccessToken { get; set; }
        [JsonPropertyName("exp")]
        public UInt64 Exp { get; set; }
        [JsonPropertyName("user_id")]
        public string Id { get; set; }
    }
}